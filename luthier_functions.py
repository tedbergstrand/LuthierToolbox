"""
Luthier's Toolbox luthier_functions.py

This code provides a collection of functions used for my Luthier Toolbox apps, a set of web-based tools for guitar building and repair. These functions are designed to perform calculations and conversions commonly used in the field of luthierie.

The code is released under the GNU General Public License v3 (GPL-3.0), which grants users the freedom to use, modify, and distribute the code under certain conditions. Please refer to the full license text for more information.

For more, visit the repository at: https://github.com/tedbergstrand/LuthierToolbox

2023 Ted Bergstrand
"""



from fractions import Fraction

def round_to_denominator(fraction_value, denominator=64):
    """
    Rounds a given fraction to the nearest denominator found on a ruler.

    Args:
        fraction_value (float): The value of the fraction as a decimal number.
        denominator (int, optional): The smallest denominator to consider. Default is 64.

    Returns:
        Fraction: The rounded fraction using the nearest denominator found on the ruler.

    Example:
        >>> round_to_denominator(0.45)
        Fraction(9, 20)
    """
	
    # If the fraction value is 0, return 0 with the specified denominator
    if fraction_value == 0:
        return Fraction(0, denominator)

    # If the fraction value is negative, store the sign and make the value positive
    elif fraction_value < 0:
        sign = -1
        fraction_value = abs(fraction_value)
    else:
        sign = 1

    # Set of standard denominators to consider
    standard_denominators = {2, 4, 8, 16, 32, denominator}

    # Calculate the numerator by rounding the fraction value multiplied by the denominator
    numerator = round(fraction_value * denominator)

    # Create a Fraction object using the calculated numerator and denominator
    fraction = Fraction(numerator, denominator)

    # Check if the denominator is one of the standard ruler denominators or the specified denominator
    if fraction.denominator in standard_denominators:
        # If the denominator is found, return the fraction with the sign
        return sign * fraction

    # If no suitable denominator is found, return the input value with the sign
    return sign * fraction_value




import re
from fractions import Fraction

def input_to_inches(input_value):
	"""
	Converts an input value string to decimal inches.

	Args:
	    input_value (str): The input value to be converted.

	Returns:
	    float: The converted value in decimal inches.

	Raises:
	    None

	The function takes an input value string and converts it to decimal inches. The input value can include various units
	such as inches, millimeters, centimeters, meters, feet, yards, kilometers, microns, or miles. The input value can also
	be in different formats including decimal numbers, fractions, or mixed fractions. It's designed to take input in any 
	way you'd write it down.

	The function first performs some string manipulation to ensure consistency in parsing. It replaces any apostrophes
	with "ft" for unit consistency and replaces commas with decimals for non-American users. The " symbol for inches is 
 	ignored because any unknown unit will default to inches.

	The input value is then parsed using a regular expression pattern, which extracts the numeric value and the unit
	from the input string. The extracted numeric value is converted to a float, taking into account different formats
	such as decimal numbers, fractions, or mixed fractions.

	The unit is matched with a dictionary mapping unit abbreviations to full names. If the unit is not recognized, it
	defaults to inches.

	A dictionary is defined to map units to conversion factors relative to inches. The input value is then converted to
	decimal inches by dividing the numeric value by the appropriate conversion factor based on the unit.

	The resulting decimal inch value is returned as a float.
	"""

	# Replace any apostrophes with "ft" for consistency in parsing.
	# Also replace commas with decimals for European users.
	# Since the code defaults to inches, no matching is done for the " inch unit.
	input_value = input_value.replace("'", "ft").replace(",", ".")

	# Define the regular expression pattern for parsing the input value
	# The pattern consists of three main parts:
	# - ((\d+\s)?\d+/\d+): Matches mixed numbers (e.g., "1 1/2") or fractions (e.g., "1/2")
	# - (\d+(\.\d+)?): Matches decimal numbers with optional decimal places (e.g., "1.5" or "3")
	# - (\.\d+): Matches decimal numbers without leading digits (e.g., ".5")
	# - \s*: Matches optional whitespace characters between the numeric value and the unit
	# - ([a-zA-Z]+)?: Matches an optional unit composed of one or more alphabetical characters
	# The pattern allows for flexible matching of various numeric formats and units in the input value

	pattern = r'((\d+\s)?\d+/\d+|\d+(\.\d+)?|\.\d+)\s*([a-zA-Z]+)?'
	match = re.match(pattern, input_value)
	if match:
		# Extract the numeric value from the input string
		value_str = match.group(1)

		# Check if the value is a mixed fraction (e.g. "1 1/2")
		if '/' in value_str and ' ' in value_str:
			whole_num, frac = value_str.split(' ')
			numerator, denominator = frac.split('/')
			value = float(whole_num) + float(numerator)/float(denominator)
		
		# Check if the value is a fraction (e.g. "1/2")
		elif '/' in value_str:
			value = float(Fraction(value_str))
		
		# Otherwise, the value is already a decimal or integer (e.g. "1.5" or "1")
		else:
			value = float(value_str)

		# Extract the unit from the input string
		unit = match.group(4)

		# Define a dictionary mapping unit abbreviations to full names
		unit_map = {
			'in': 'inches',
			'inch': 'inches',
			'inches': 'inches',
			'mm': 'millimeters',
			'millimeter': 'millimeters',
			'millimeters': 'millimeters',
			'cm': 'centimeters',
			'centimeter': 'centimeters',
			'centimeters': 'centimeters',
			'm': 'meters',
			'meter': 'meters',
			'meters': 'meters',
			'ft': 'feet',
			'foot': 'feet',
			'feet': 'feet',
			'yd': 'yards',
			'yard': 'yards',
			'yards': 'yards',
			'km': 'kilometers',
			'kilometers': 'kilometers',
			'micron': 'microns',
			'micrometers': 'microns',
			'microns': 'microns',
			'um': 'microns',
			'mi': 'miles',
			'mile': 'miles',
			'miles': 'miles'
			}
	# Get the full unit name from the unit map, defaulting to inches if the unit is not recognized
	unit = unit_map.get(unit, 'inches')

	# Define a dictionary mapping units to conversion factors relative to inches
	conversions = {
		'inches': 1,
		'millimeters': 25.4,
		'centimeters': 2.54,
		'meters': 0.0254,
		'feet': 1/12,
		'yards': 1/36,
		'kilometers': 0.0000254,
		'microns': 25400,
		'miles': 1/63360
	}

	# Convert the input value to decimal inches
	decimal_inch = value / conversions[unit]

	return decimal_inch


from fractions import Fraction

def convert(input_value):
    """
    Convert an input value to various units of measurement.

    Args:
        input_value (str): The input value to be converted. It should be in the form of '3 in', '3mm', '4 feet', '8"', etc.

    Returns:
        dict: A dictionary containing the converted values in different units. The keys of the dictionary represent the unit names, and the values represent the converted measurements as strings.

    Note:
        - The fractional output is not a true conversion. It represents the closest measurement on a ruler.
        - Commas are replaced with decimals for non-American users and unit-matching & conversion are done via the input_to_inches function.

    TODO:
        - Add regular proper fractional output (non-ruler)?
    """

    # Convert the input value to decimal inches
    decimal_inch = input_to_inches(input_value)

    # Convert the decimal inches to a fractional inches with a maximum denominator of 64
    fractional_inch = Fraction(decimal_inch).limit_denominator(64)

    # Round the fractional inches to the nearest standard ruler denominator
    rounded_fraction = round_to_denominator(fractional_inch)

    # Generate the output string for the fractional inch value
    if rounded_fraction.numerator == int(rounded_fraction):
        # If the rounded fraction is an integer, just use the whole number of inches
        mixed_number = f"{int(decimal_inch):d}"
    else:
        if rounded_fraction.numerator >= rounded_fraction.denominator * 2 or decimal_inch >= 1:
            # If the rounded fraction is greater than or equal to 1/2 or the decimal inches is greater than 1,
            # use a mixed number format (e.g. "1 1/2")
            mixed_number = f"{int(decimal_inch)} {Fraction(rounded_fraction % 1)}"
        else:
            # Otherwise, use a simple fraction format (e.g. "1/2")
            mixed_number = f"{Fraction(rounded_fraction)}"

    # Define a dictionary mapping units to conversion factors relative to inches
    conversions = {
        'inches': 1,
        'millimeters': 25.4,
        'centimeters': 2.54,
        'meters': 0.0254,
        'feet': 1/12,
        'yards': 1/36,
        'kilometers': 0.0000254,
        'microns': 25400,
        'miles': 1/63360
    }

    # Define a dictionary mapping unit names to their respective values
    conversions_dict = {
        'microns': f"{decimal_inch*conversions['microns']:.1f} µm",
        'decimal': f"{decimal_inch:.3f} in",
        'fraction': f"{mixed_number} in",
        'feet': f"{decimal_inch*conversions['feet']:.3f} ft",
        'yards': f"{decimal_inch*conversions['yards']:.3f} yd",
        'miles': f"{decimal_inch*conversions['miles']:.3f} mi",
        'millimeters': f"{decimal_inch*conversions['millimeters']:.2f} mm",
        'centimeters': f"{decimal_inch*conversions['centimeters']:.2f} cm",
        'meters': f"{decimal_inch*conversions['meters']:.3f} m",
        'kilometers': f"{decimal_inch*conversions['kilometers']:.3f} km"
    }

    # Return the dictionary of conversions
    return conversions_dict



from decimal import Decimal, getcontext

def calculate_spacing(nut_width, string_gauges, edge_distance=Decimal('0.125'), edge_checkbox=False):
    """
    Calculate the spacing between strings on a guitar.

    Parameters:
    - nut_width (decimal): The width of the nut in inches.
    - string_gauges (list): List of string gauges in inches, from low to high.
    - edge_distance (decimal, optional): The distance between the outermost strings and the edge of the nut. Default is 0.125 inches.
    - edge_checkbox (bool, optional): Indicates whether to use the edge distance directly for the low E and high E strings. Default is False.

    Returns:
    - inter_string_distance (decimal): The distance between adjacent strings.
    - positions (list): List of positions representing the middle point of each string.

    This function calculates the spacing between strings on a guitar based on the nut width, string gauges,
    and the optional parameters for edge distance calculation. It returns the inter-string distance and the
    positions of the middle point of each string.

    If `edge_checkbox` is set to True, the edge distance will be directly used for the low E and high E strings.
    Otherwise, the edge distance is adjusted based on half of the gauge of the outermost strings.

    The calculation is performed as follows:
    1. Calculate the positions of the outside edges of the low E and high E strings.
    2. Calculate the positions of the inside edges of the low E and high E strings.
    3. Calculate the total inside distance between the inside edges of the low E and high E strings.
    4. Subtract the sum of the diameters of the interior strings from the total inside distance.
    5. Divide the distance calculated in the previous step by the number of strings minus one to get the inter-string distance.
    6. Calculate the positions of the leading and trailing edges of each string.

    Example usage:
    nut_width = Decimal('1.625')
    string_gauges = [Decimal('0.046'), Decimal('0.036'), Decimal('0.026'), Decimal('0.017'), Decimal('0.013'), Decimal('0.010')]
    inter_string_distance, positions = calculate_spacing(nut_width, string_gauges, edge_distance=Decimal('0.125'), edge_checkbox=False)
    """

    # Set the precision to 4 decimal places (6 digits)
    getcontext().prec = 6

    # Calculate the positions of the outside edges of the low E and high E strings
    if edge_checkbox:
        low_e_edge = Decimal(edge_distance)
        high_e_edge = Decimal(nut_width) - Decimal(edge_distance)
    else:
        low_e_edge = Decimal(edge_distance) - (Decimal(string_gauges[0]) / Decimal('2'))
        high_e_edge = Decimal(nut_width) - Decimal(edge_distance) + (Decimal(string_gauges[-1]) / Decimal('2'))

    # calculate the positions of the inside edges of the low E and high E strings
    low_e_inside = low_e_edge + Decimal(string_gauges[0])
    high_e_inside = high_e_edge - Decimal(string_gauges[-1])

    # calculate the total inside distance between the inside edges of the low E and high E strings
    total_inside_distance = high_e_inside - low_e_inside

    # subtract the sum of the diameters of the interior strings from our total inside distance
    interior_diameters = Decimal(sum(string_gauges[1:-1]))
    inside_distance = total_inside_distance - interior_diameters

    # divide the distance calculated in the previous step by the number of strings to get the inter-string distance
    inter_string_distance = inside_distance / Decimal(len(string_gauges) - 1)

    # calculate the positions of the leading and trailing edges of each string
    positions = []
    position = low_e_edge
    for gauge in string_gauges:
        positions.append((position + position + Decimal(gauge)) / Decimal('2'))
        position += inter_string_distance + Decimal(gauge)

    return inter_string_distance, positions

def fret_placement(scale_length, fret_number):
    """
    Calculates the placement of a fret on a stringed instrument based on the scale length and fret number. Works with either metric or inches.

    Args:
        scale_length (float): The length of the vibrating portion of the string, typically measured from the nut to the bridge.
        fret_number (int): The number of the fret on the instrument. 0 represents the nut, and higher numbers represent frets closer to the bridge.

    Returns:
        float: The distance from the nut to the center of the specified fret, measured along the string.

    Example:
        >>> fret_placement(25.5, 12)
        12.7844969284613

    The function simply performs the fret placement math that everyone uses.

    The `scale_length` argument should be a positive float representing the length of the string in inches or any other unit of measurement.
    The `fret_number` argument should be a non-negative integer representing the fret number.

    Note:
    - This formula assumes a standard equal temperament tuning system.
    """
    return scale_length - (scale_length / (2 ** (fret_number / 12)))

def calculate_fretboard(start_radius, end_radius, scale_length, num_frets):
    """
    Calculate the positions and radii of frets on a guitar fretboard.

    Args:
        start_radius (float): The starting radius of the fretboard at the nut.
        end_radius (float): The ending radius of the fretboard at the end of the extension (assumed to be one fret past your last fret).
        scale_length (float): The scale length of the guitar.
        num_frets (int): The number of frets on the fretboard.

    Returns:
        dict: A dictionary containing the following keys:
            - 'fretboard_length' (float): The length of the fretboard.
            - 'saddle_radius' (float): The radius of the saddle.
            - 'result' (list): A list of tuples representing the positions and radii of each fret.
                Each tuple contains two elements:
                    - The position of the fret.
                    - The radius of the fret.
                    """
    fretboard_length = fret_placement(scale_length, num_frets + 1)
    final_fret_pos = fret_placement(scale_length, num_frets)

    final_radius = start_radius + (final_fret_pos / fretboard_length) * (end_radius - start_radius)

    saddle_radius = start_radius + (scale_length / fretboard_length) * (end_radius - start_radius)

    positions = [fret_placement(scale_length, fret) for fret in range(1, num_frets + 1)]
    result = [(pos, start_radius + (pos / fretboard_length) * (end_radius - start_radius)) for pos in positions[:-1]]
    result.append((final_fret_pos, final_radius))

    return {
        'fretboard_length': fretboard_length,
        'saddle_radius': saddle_radius,
        'result': result
    }
