from deep_translator import GoogleTranslator


def translate_to_chines(paragraph: str) -> str:
    """translate text with google API to chines"""
    return GoogleTranslator(source="auto", target="zh-CN").translate(paragraph)


def write_output_file(content: str):
    """write the content param to an output file in utf-8 format"""
    with open("output.txt", encoding="utf-8", mode="w") as output_file:
        output_file.write(content)


def get_file_content(path: str):
    """read file content by path"""
    with open(path, encoding="utf-8", mode="r") as file:
        text = file.read()
        return text


def guess_game() -> None:
    """invoke app"""
    try:
        file_path = input(
            "please type the file name and ext: like [name].[ext] that you want to translate: "
        )
        text = get_file_content(file_path)
        translation = translate_to_chines(text)

        write_output_file(translation)
    except FileNotFoundError as err:
        print(f"file not found {err}")

    except Exception as err:
        print(f"internal err {err}")


if __name__ == "__main__":
    guess_game()
