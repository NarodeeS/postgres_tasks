from pages.login_page import LogintPage


def test_logout_page(browser):
    login_page = LogintPage(browser)
    login_page.open()
    login_page.send_form()

    assert login_page.check_curent_url() == 'http://localhost/account', "Login failed"
    assert login_page.find_logout_button_if_exists() == 'Logout', "Login failed"
    assert login_page.find_task_list_if_exists() == True, "Registration failed"

