import streamlit as st
import json, os
from datetime import date

FILE="tasks.json"
st.set_page_config(page_title="To-Do Manager",page_icon="📝",layout="wide")

def load_tasks():
    if not os.path.exists(FILE):
        with open(FILE,"w") as f:
            json.dump([],f)
    with open(FILE,"r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(FILE,"w") as f:
        json.dump(tasks,f,indent=4)

tasks=load_tasks()

st.sidebar.title(" To-Do Manager")
page=st.sidebar.radio("Menu",["Add Task","View Tasks","Update Task","Delete Task"])
st.title(" To-Do Manager")

if page=="Add Task":
    task=st.text_input("Task Name")
    desc=st.text_area("Description")
    due=st.date_input("Due Date",date.today())
    priority=st.selectbox("Priority",["Low","Medium","High"])
    if st.button("Add Task"):
        if not task.strip():
            st.warning("Enter task name.")
        elif any(t["task"].lower()==task.lower() for t in tasks):
            st.error("Task already exists.")
        else:
            tasks.append({"task":task,"description":desc,"due":str(due),"priority":priority,"status":"Pending"})
            save_tasks(tasks)
            st.success("Task added.")

elif page=="View Tasks":
    search=st.text_input("Search")
    c1,c2,c3=st.columns(3)
    total=len(tasks)
    completed=sum(1 for t in tasks if t["status"]=="Completed")
    c1.metric("Total",total)
    c2.metric("Completed",completed)
    c3.metric("Pending",total-completed)
    for t in tasks:
        if search.lower() in t["task"].lower():
            with st.expander(t["task"]):
                st.write(t)

elif page=="Update Task":
    if tasks:
        names=[t["task"] for t in tasks]
        sel=st.selectbox("Task",names)
        i=names.index(sel)
        new_name=st.text_input("Name",tasks[i]["task"])
        new_desc=st.text_area("Description",tasks[i]["description"])
        new_status=st.selectbox("Status",["Pending","Completed"], index=0 if tasks[i]["status"]=="Pending" else 1)
        if st.button("Update"):
            tasks[i]["task"]=new_name
            tasks[i]["description"]=new_desc
            tasks[i]["status"]=new_status
            save_tasks(tasks)
            st.success("Updated.")
    else:
        st.info("No tasks.")

elif page=="Delete Task":
    if tasks:
        names=[t["task"] for t in tasks]
        sel=st.selectbox("Delete Task",names)
        if st.button("Delete"):
            tasks=[t for t in tasks if t["task"]!=sel]
            save_tasks(tasks)
            st.success("Deleted.")
    else:
        st.info("No tasks.")
