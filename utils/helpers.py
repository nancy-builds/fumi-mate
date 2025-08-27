import random
import string
import datetime
import json
import os


# ========== GENERAL UTILITIES ==========

def generate_random_string(length=8):
    """Generate a random string of given length (default 8)."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def get_current_year():
    """Return the current year as integer."""
    return datetime.datetime.now().year


def slugify(text):
    """Convert text into a URL-friendly slug."""
    return text.lower().replace(" ", "-").replace("_", "-")


def format_datetime(dt=None, fmt="%Y-%m-%d %H:%M:%S"):
    """Format datetime into a string."""
    if dt is None:
        dt = datetime.datetime.now()
    return dt.strftime(fmt)


def paginate_items(items, page=1, per_page=10):
    """Paginate a list of items."""
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end]


# ========== FLASHCARDS ==========

def shuffle_flashcards(cards):
    """Shuffle flashcards list and return."""
    random.shuffle(cards)
    return cards


def calculate_score(correct, total):
    """Calculate percentage score for flashcard/game results."""
    if total == 0:
        return 0
    return round((correct / total) * 100, 2)


# ========== BLOG UTILITIES ==========

BLOG_FILE = "data/blog_posts.json"  # you can change path


def get_excerpt(content, length=100):
    """Return a short excerpt from a blog post."""
    return content[:length] + "..." if len(content) > length else content


def save_blog_post(title, content, author="Anonymous"):
    """Save a blog post into a JSON file."""
    post = {
        "title": title,
        "slug": slugify(title),
        "content": content,
        "author": author,
        "created_at": format_datetime()
    }

    posts = load_blog_posts()
    posts.append(post)

    os.makedirs(os.path.dirname(BLOG_FILE), exist_ok=True)
    with open(BLOG_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)

    return post


def load_blog_posts():
    """Load blog posts from JSON file."""
    if os.path.exists(BLOG_FILE):
        with open(BLOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


# ========== PROFILE UTILITIES ==========

PROFILE_FILE = "data/profile.json"


def validate_profile_data(data):
    """Validate profile fields (basic check)."""
    required_fields = ["name", "email"]
    for field in required_fields:
        if field not in data or not data[field]:
            return False
    return True


def get_user_profile():
    """Get user profile from file."""
    if os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"name": "", "email": "", "bio": ""}


def update_user_profile(data):
    """Update and save user profile."""
    if not validate_profile_data(data):
        return None

    os.makedirs(os.path.dirname(PROFILE_FILE), exist_ok=True)
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return data


# ========== GAME UTILITIES ==========

def generate_question(level=1):
    """Generate a random math question for game."""
    if level == 1:
        a, b = random.randint(1, 10), random.randint(1, 10)
        return f"{a} + {b}", a + b
    elif level == 2:
        a, b = random.randint(5, 20), random.randint(5, 20)
        return f"{a} - {b}", a - b
    else:
        a, b = random.randint(2, 12), random.randint(2, 12)
        return f"{a} x {b}", a * b


def check_answer(user_answer, correct_answer):
    """Check if user answer is correct."""
    return str(user_answer).strip() == str(correct_answer).strip()
