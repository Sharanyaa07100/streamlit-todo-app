import streamlit as st

st.title("📝 My To-Do List")

# Initialize task list
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# New task input
new_task = st.text_input("Add a new task:")

# Add task button
if st.button("➕ Add Task"):
    if new_task.strip() != "":
        st.session_state.tasks.append({"task": new_task, "done": False})
    else:
        st.warning("Task cannot be empty!")

# Show tasks
st.subheader("Your Tasks:")
for i, task in enumerate(st.session_state.tasks):
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        checked = st.checkbox("", key=i, value=task["done"])
        st.session_state.tasks[i]["done"] = checked
    with col2:
        st.markdown(f"{'✅ ' if task['done'] else '🔲 '}{task['task']}")

# Clear completed button
if st.button("🗑️ Clear Completed"):
    st.session_state.tasks = [t for t in st.session_state.tasks if not t["done"]]

