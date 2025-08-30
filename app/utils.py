import datetime

def extract_metadata(file):
    mime = file.get("mimeType", "")
    if mime.startswith("image/"):
        type_tag = "#photo"
    elif mime.startswith("video/"):
        type_tag = "#video"
    else:
        type_tag = "#other"
    media_md = file.get("imageMediaMetadata", {}) or file.get("videoMediaMetadata", {})
    dt = (
        media_md.get("time")
        or file.get("createdTime")
        or file.get("modifiedTime")
    )
    def normalize(d):
        try:
            return datetime.datetime.fromisoformat(d).strftime("%Y-%m-%d")
        except Exception:
            return "unknown"
    created_ymd = normalize(dt)
    return dict(
        type_tag=type_tag,
        created_ymd=created_ymd,
        original_name=file.get("name"),
    )

def render_caption(template, author_tag, type_tag, created_ymd, original_name):
    return template.format(
        author_tag=author_tag,
        type_tag=type_tag,
        created_ymd=created_ymd,
        original_name=original_name,
    )

def match_filters(file, filters):
    if filters.get("min_size") and int(file.get("size", 0)) < filters["min_size"]:
        return False
    mime = file.get("mimeType", "")
    if filters.get("include_mime") and not any(mime.startswith(m) for m in filters["include_mime"]):
        return False
    if filters.get("exclude_mask") and any(x in file["name"] for x in filters["exclude_mask"]):
        return False
    return True
