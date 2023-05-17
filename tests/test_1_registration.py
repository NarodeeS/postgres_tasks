from pages.registration_page import RegistrationPage

def test_registration_page(browser):
    registration_page = RegistrationPage(browser)
    registration_page.open()
    registration_page.send_form()

    assert registration_page.check_curent_url() == 'http://localhost/account', "Login failed"
    assert registration_page.find_logout_button_if_exists() == 'Logout', "Login failed"
    assert registration_page.find_task_list_if_exists() == True, "Registration failed"

