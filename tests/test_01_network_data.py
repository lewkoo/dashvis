from dash.testing.application_runners import import_app
from selenium.webdriver import ActionChains
from selenium.webdriver import Keys

new_data_input = '''{
  "nodes": [
    {
      "id": 1,
      "cid": 1,
      "label": "Node 1",
      "title": "This is Node 1"
    },
    {
      "id": 2,
      "cid": 1,
      "label": "Node 2",
      "title": "This is Node 2"
    },
    {
      "id": 3,
      "cid": 1,
      "label": "Node 3",
      "title": "This is Node 3"
    }
  ],
  "edges": [
    {
      "from": 1,
      "to": 3
    },
    {
      "from": 1,
      "to": 2
    }
  ]
}
'''


def test_render_component(dash_duo):
    # Start a dash app contained as the variable `app` in `usage.py`
    app = import_app('usage_examples.01_network_data')
    dash_duo.start_server(app)

    # Get the generated component input with selenium
    # The html input will be a children of the #input dash component
    dash_duo.wait_for_element_by_id("network-data-input", timeout=None)
    data_input = dash_duo.find_element('#network-data-input > textarea')

    # ActionChains(dash_duo.get_webdriver()) \
    #     .move_to_element(data_input) \
    #     .double_click(data_input) \
    #     .key_down(Keys.CONTROL) \
    #     .send_keys('a') \
    #     .key_up(Keys.CONTROL) \
    #     .send_keys(Keys.DELETE) \
    #     .double_click(data_input) \
    #     .send_keys(new_data_input) \
    #     .perform()
    # # data_input.click()
    # # data_input.send_keys(Keys.CONTROL + "a")
    # # data_input.send_keys(Keys.DELETE)
    #
    # # data_input.send_keys(new_data_input)
    #
    # dash_duo.wait_for_text_to_equal('#network-data-input > textarea', new_data_input)
    #
    # # Clear the input
    # # dash_duo.clear_input(my_component)
    #
    # # Send keys to the custom input.
    # # my_component.send_keys('Hello dash')
    #
    # # Wait for the text to equal, if after the timeout (default 10 seconds)
    # # the text is not equal it will fail the test.
    # # dash_duo.wait_for_text_to_equal('#output', 'You have entered Hello dash')
