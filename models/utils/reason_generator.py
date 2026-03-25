def generate_detailed_reason(caption, content_type="image", category="violence"):

    caption = caption.lower()

    if category == "violence":
        return f"A person is involved in a potentially harmful or threatening situation ({caption}), which is why this {content_type} has been removed."

    elif category == "sexual_content":
        return f"The {content_type} appears to contain inappropriate or explicit visual elements ({caption}), which violates platform safety guidelines."

    else:
        return f"The {content_type} violates platform safety policies based on detected content."