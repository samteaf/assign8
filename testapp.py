import requests

# Base URL of the API
BASE_URL = 'http://localhost:4000'

# Function to send a GET request to an endpoint and check the response
def test_endpoint(endpoint, test_cases):
    tests_passed = 0
    total_tests = 0
    for element in test_cases:

        test_input = element[0]
        test_output = element[1]
        test_status = element[2]

        url = f'{BASE_URL}/{endpoint}/{test_input}'
        response = requests.get(url)
        total_tests += 1

        if response.status_code == 200: #if request successful
            result = response.json()
            if result.get('output') == test_output:
                tests_passed += 1
        elif response.status_code == test_status:  #unsuccessful request but correct test
                tests_passed += 1
        else:
            print(f'Expected Status Code: {test_status}, Actual: {response.status_code}')
        
    if total_tests == tests_passed:
        out = True
    else:
        out = False

    return(out)


# Function to run test cases for the md5 endpoint
def test_md5():
    test_cases = [
        ("hello", "5d41402abc4b2a76b9719d911017c592", 200),
        ("world", "7d793037a0760186574b0282f2f435e7", 200),
        ("devops", "a21c218df41f6d7fd032535fe20394e2", 200),
        ("is", "a2a551a6458a8de22446cc76d639a9e9", 200),
        ("culture", "3f7039a836c00d92ecf87fd7d338c4db", 200),
        (1, "c4ca4238a0b923820dcc509a6f75849b", 200),
        ("!$(@)@@", "7abcdc98202a4641e593f935454a2806", 200),
        (" ", "7215ee9c7d9dc229d2921a40e899ec5f", 200),
        ("", {"error": "Input must have some character"}, 404)
    ]
    if test_endpoint('md5', test_cases):
        return 0
    else:
        return 1
    

# Function to run test cases for the factorial endpoint
def test_factorial():
    test_cases = [
        (0, 1, 200),
        (1, 1, 200),
        (5, 120, 200),
        (8, 40320, 200),
        (10, 3628800, 200),
        (15, 1307674368000, 200),
        (500, 1220136825991110068701238785423046926253574342803192842192413588385845373153881997605496447502203281863013616477148203584163378722078177200480785205159329285477907571939330603772960859086270429174547882424912726344305670173270769461062802310452644218878789465754777149863494367781037644274033827365397471386477878495438489595537537990423241061271326984327745715546309977202781014561081188373709531016356324432987029563896628911658974769572087926928871281780070265174507768410719624390394322536422605234945850129918571501248706961568141625359056693423813008856249246891564126775654481886506593847951775360894005745238940335798476363944905313062323749066445048824665075946735862074637925184200459369692981022263971952597190945217823331756934581508552332820762820023402626907898342451712006207714640979456116127629145951237229913340169552363850942885592018727433795173014586357570828355780158735432768888680120399882384702151467605445407663535984174430480128938313896881639487469658817504506926365338175055478128640000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000, 200),
        ('10!', {"error": "Input must be a whole number"}, 404),
        ('xyz', {"error": "Input must be a whole number"}, 404),
        (2.3, {"error": "Input must be a whole number"}, 404),
        (-5, {"error": "Input must be a whole number"}, 404),
        (100, 93326215443944152681699238856266700490715968264381621468592963895217599993229915608941463976156518286253697920827223758251185210916864000000000000000000000000, 200)
    ]
    if test_endpoint('factorial', test_cases):
        return 0
    else:
        return 1

# Function to run test cases for the fibonacci endpoint
def test_fibonacci():
    test_cases = [
        (0, [0], 200),
        (1, [0, 1, 1], 200),
        (10, [0, 1, 1, 2, 3, 5, 8], 200),
        (-1, [], 404),
        (50, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34], 200),
        (100, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89], 200),
        (200, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144], 200),
        (1000, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987], 200),
        (1.5, {"error": "Input must be a non-negative integer"}, 404),
        (-5, {"error": "Input must be a non-negative integer"}, 404),
        ('abc', {"error": "Input must only contain non-negative integers"}, 404),
        ('5$', {"error": "Input must only contain non-negative integers"}, 404),
        ('', {"error": "Input must be a non-negative integer"}, 404),
    ]
    if test_endpoint('fibonacci', test_cases):
        return 0
    else:
        return 1

# Function to run test cases for the is-prime endpoint
def test_is_prime():
    test_cases = [
        (0, False),
        (1, False),
        (2, True),
        (9, False),
        (11, True),
        (16, False), 
        (23, True),   
        (100, False), 
        (97, True),   
        (50, False),  
    ]
    
    tests_passed = 0
    total_tests = 0
    
    for test_input, expected_output in test_cases:
        url = f'{BASE_URL}/is-prime/{test_input}'
        response = requests.get(url)
        total_tests += 1
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('is_prime') == expected_output:
                tests_passed += 1
            else:
                print('Test failed for input={}, expected={}, actual={}'.format(test_input, expected_output, result.get('is_prime')))
        else:
            print('Request failed for input={}'.format(test_input))
    
    if tests_passed == total_tests:
        return 0
    else:
        return 1

def test_slack_alert():
    test_cases = [
        ("Automation Test 1"),
        ("Automation Test 2"),
    ]

    tests_passed = 0
    total_tests = 0

    for message in test_cases:
        url = f'{BASE_URL}/slack-alert/{message}'
        response = requests.get(url)
        total_tests += 1

        if response.status_code == 200:
            result = response.json()
            if 'success' in result and result['success'] is True:
                tests_passed += 1
            else:
                print(f'Slack test failed for message: {message}')
        else:
            print(f'Request to Slack failed for message: {message}')

    if tests_passed == total_tests:
        return 0
    else:
        return 1

def test_key_val():
    test_cases = []
    

if __name__ == '__main__':
    print('md5: ', test_md5())
    print('factorial: ', test_factorial())
    print('fibonacci: ', test_fibonacci())
    print('is-prime: ', test_is_prime())
    print('slack-alert: ', test_slack_alert())