import random
import streamlit as st

# ---------- Page Setup ----------
st.set_page_config(
    page_title="Kind To-Do",
    page_icon="🌱",
    layout="centered"
)

st.markdown(
    """
    <style>
        div[data-testid="stMetric"] {
            border: 1px solid rgba(128, 128, 128, 0.22);
            padding: 12px 14px;
            border-radius: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Memory ----------
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "next_id" not in st.session_state:
    st.session_state.next_id = 1

boosts = [
    "Small steps still move you forward! 🚶",
    "Helping one person today makes the world better. 🌍",
    "Done is better than perfect. ✅",
    "You've got this! 💪",
    "Kindness is a task worth doing every day. 💛"
]

# ---------- Functions ----------
def is_duplicate(title):
    for task in st.session_state.tasks:
        if task["title"].lower() == title.lower():
            return True
    return False


def get_icon(priority):
    if priority == "high":
        return "🔴"
    elif priority == "medium":
        return "🟡"
    return "🟢"


def toggle_task(task_id, done):
    for t in st.session_state.tasks:
        if t["id"] == task_id:
            t["done"] = done
            break


def delete_task(task_id):
    st.session_state.tasks = [
        t for t in st.session_state.tasks if t["id"] != task_id
    ]


# ---------- Header ----------
st.title("🌱 Kind To-Do")
st.caption("Plan your day, and help someone else too.")

if st.button("✨ Give me a boost"):
    st.session_state.boost = random.choice(boosts)

if "boost" in st.session_state:
    st.info(st.session_state.boost)

st.divider()

# ---------- Stats ----------
tasks = st.session_state.tasks
total = len(tasks)
done_count = sum(task["done"] for task in tasks)
pending_count = total - done_count

col1, col2, col3 = st.columns(3)
col1.metric("Total", total)
col2.metric("Done", done_count)
col3.metric("Pending", pending_count)

st.divider()

# ---------- Add a Task ----------
st.subheader("➕ Add a task")

with st.form("task_form", clear_on_submit=True):
    title = st.text_input("Task title")

    helping = st.text_input(
        "Who is this for?",
        placeholder="Leave empty if it's for you"
    )

    priority = st.selectbox(
        "Priority",
        ["high", "medium", "low"],
        index=2
    )

    submitted = st.form_submit_button("Add task", type="primary", use_container_width=True)

    if submitted:
        clean_title = title.strip()

        if clean_title == "":
            st.warning("Please type a task title first.")

        elif is_duplicate(clean_title):
            st.error("This task is already in your list!")

        else:
            who = helping.strip() or "Me"

            st.session_state.tasks.append({
                "id": st.session_state.next_id,
                "title": clean_title,
                "for": who,
                "priority": priority,
                "done": False
            })
            st.session_state.next_id += 1

            st.success("Task added successfully!")
            st.rerun()

st.divider()

# ---------- Show Tasks ----------
st.subheader("📋 Your tasks")

if not tasks:
    st.info("Nothing here yet. Add your first task above!")

else:
    st.progress(done_count / total if total else 0)
    st.write(
        f"**Progress: {done_count} of {total} tasks done**"
    )

    for task in tasks:
        task_id = task["id"]
        with st.container(border=True):
            col1, col2 = st.columns([5, 1])

            with col1:
                checked = st.checkbox(
                    f"{get_icon(task['priority'])} {task['title']}",
                    value=task["done"],
                    key=f"done_{task_id}",
                )

                if checked != task["done"]:
                    toggle_task(task_id, checked)
                    st.rerun()

                st.caption(f"For: {task['for']}")

                if task["done"]:
                    st.success("Completed")

            with col2:
                if st.button("🗑️", key=f"delete_{task_id}"):
                    delete_task(task_id)
                    st.rerun()

st.divider()

st.caption("🌱 Small steps. Kind actions. Better days.")
