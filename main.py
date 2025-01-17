import os
import time
import pypandoc
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService


def fetch_stepik_content(url, sessionid, chromedriver_path, chromium_path):
    options = Options()
    options.binary_location = chromium_path  # Укажите путь к вашему бинарнику Chromium
    options.add_argument("--headless")  # Запуск в фоновом режиме
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Используйте webdriver-manager для установки драйвера
    service = ChromeService(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Установите cookie перед загрузкой страницы
        driver.get("https://stepik.org")
        driver.add_cookie({'name': 'sessionid', 'value': sessionid, 'domain': '.stepik.org'})

        # Перейдите на нужный URL
        driver.get(url)
        time.sleep(10)  # Пауза для загрузки JavaScript-контента

        content = driver.find_element(By.CLASS_NAME, 'step-dynamic-container')
        return content.get_attribute('innerHTML')
    finally:
        driver.quit()


def convert_html_to_format(html_content, output_format):
    try:
        return pypandoc.convert_text(html_content, output_format, format='html')
    except RuntimeError as e:
        print(f"Error during conversion: {e}")
        return None


def save_to_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)


def main():
    supported_formats = {
        "org": "Emacs Org Mode",
        "markdown": "Markdown format",
        "html": "HTML document",
        "pdf": "PDF document (requires LaTeX)",
        "docx": "MS Word document",
        "rst": "reStructuredText"
    }
    parser = argparse.ArgumentParser(description='Fetch and convert Stepik course content.')
    parser.add_argument('url', help='URL of the Stepik course')
    parser.add_argument('--sessionid', required=True, help='Your Stepik session ID')
    parser.add_argument('--chromedriver-path', required=True, help='Path to your ChromeDriver executable')
    parser.add_argument('--chromium-path', required=True, help='Path to your Chromium binary')
    parser.add_argument(
        '--format',
        required=True,
        choices=supported_formats.keys(),
        help=f"Desired output format: {', '.join([f'{fmt} ({desc})' for fmt, desc in supported_formats.items()])}"
    )
    parser.add_argument(
        '-o', '--output',
        help='Name of the output file. If not provided, a default name will be used based on the chosen format.'
    )
    parser.add_argument(
        '--output-dir',
        default='.',
        help='Directory to save the output file. Defaults to the current directory if not provided.'
    )

    args = parser.parse_args()

    html_content = fetch_stepik_content(args.url, args.sessionid, args.chromedriver_path, args.chromium_path)

    if not html_content:
        print("Failed to retrieve content.")
        return

    output_filename = args.output if args.output else f"stepik_content.{args.format}"
    output_filepath = os.path.join(args.output_dir, output_filename)
    converted_content = convert_html_to_format(html_content, args.format)

    if converted_content:
        save_to_file(output_filepath, converted_content)
        print(f"Content saved to {output_filename}")
    else:
        print("Conversion failed.")


if __name__ == "__main__":
    main()