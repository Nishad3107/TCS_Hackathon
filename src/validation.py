"""
Activity validation module for verifying places and attractions.
"""
from tools import validate_place
from schemas import TravelItinerary
import logging

logger = logging.getLogger(__name__)

def validate_itinerary_activities(itinerary: TravelItinerary, sample_validation: bool = True) -> dict:
    """
    Validates activities in the itinerary to check if places exist.
    
    Args:
        itinerary: The travel itinerary to validate
        sample_validation: If True, only validates a sample of activities to save API calls
    
    Returns:
        A dictionary with validation results and warnings
    """
    validation_results = {
        "validated": [],
        "unverified": [],
        "warnings": []
    }
    
    destination = itinerary.request.destination
    activities_to_check = []
    
    # Extract specific place names from activities (simplified approach)
    for day in itinerary.days:
        activities_to_check.extend([
            day.morning_activity,
            day.afternoon_activity,
            day.evening_activity
        ])
    
    # If sample validation, only check first few activities
    if sample_validation and len(activities_to_check) > 3:
        activities_to_check = activities_to_check[:3]
        logger.info(f"Performing sample validation on {len(activities_to_check)} activities")
    
    for activity in activities_to_check:
        # Extract potential place names (simple heuristic: look for capitalized words)
        words = activity.split()
        potential_places = [word.strip('.,!?()') for word in words if word[0].isupper() and len(word) > 3]
        
        if potential_places:
            # Check the first notable place mentioned
            place_name = potential_places[0]
            result = validate_place(place_name, destination)
            
            if result['exists']:
                validation_results['validated'].append({
                    'activity': activity[:50] + '...' if len(activity) > 50 else activity,
                    'place': place_name,
                    'status': 'verified'
                })
            elif result['exists'] is False:
                validation_results['unverified'].append({
                    'activity': activity[:50] + '...' if len(activity) > 50 else activity,
                    'place': place_name,
                    'status': 'not found'
                })
                validation_results['warnings'].append(
                    f"Could not verify '{place_name}' - please double-check this location"
                )
            else:
                validation_results['unverified'].append({
                    'activity': activity[:50] + '...' if len(activity) > 50 else activity,
                    'place': place_name,
                    'status': 'validation unavailable'
                })
    
    return validation_results


def format_validation_report(validation_results: dict) -> str:
    """
    Formats validation results into a readable report.
    """
    report = "## Activity Validation Report\n\n"
    
    if validation_results['validated']:
        report += "✅ **Verified Places:**\n"
        for item in validation_results['validated']:
            report += f"- {item['place']}\n"
        report += "\n"
    
    if validation_results['unverified']:
        report += "⚠️ **Unverified Places:**\n"
        for item in validation_results['unverified']:
            report += f"- {item['place']} ({item['status']})\n"
        report += "\n"
    
    if validation_results['warnings']:
        report += "⚠️ **Warnings:**\n"
        for warning in validation_results['warnings']:
            report += f"- {warning}\n"
        report += "\n"
    
    if not validation_results['validated'] and not validation_results['unverified']:
        report += "ℹ️ No specific places were validated in this sample.\n\n"
    
    return report
