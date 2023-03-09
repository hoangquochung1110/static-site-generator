---
title: Manage State in ReactJS with to-do app
date: 2022-03-10 10:00
description: Tutorial to make a React to-do app with live deployment
category: blog
tags:
  - reactjs
---

In this post, let's examine how to use useState to manage state in a react component. State is one of two major pillars of React, it's simply what we use to handle values that change over time, the value of a counter for instance.

## useState hook
Hooks are a new feature in React 16.8. They allow us to use state (and other features) without writing a class component. Therefore, when it comes to using hooks, it means you're going to have functional components.

## Let's get started
Our to-do list app is made of two main components **App** and **Overview**. The app should render an input field and a submit button. You can add a few to-do items and they should be shown in numerical order. Note that we will use `<ul>` tag to display list item. Yes, we can make an order list by using `<ol>` but in this guide we wanna know how to manage states with useState so let's move on with `<ul>`.

<iframe src="https://codesandbox.io/embed/mystifying-golick-wkf3e?fontsize=14&hidenavigation=1&theme=dark"
     style="width:100%; height:500px; border:0; border-radius: 4px; overflow:hidden;"
     title="mystifying-golick-wkf3e"
     allow="accelerometer; ambient-light-sensor; camera; encrypted-media; geolocation; gyroscope; hid; microphone; midi; payment; usb; vr; xr-spatial-tracking"
     sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"
></iframe>

### App component

```jsx
// App component to handle input form with the logic
import './App.css';
import Overview from './components/Overview';
import { useState } from 'react';
import uniqid from "uniqid";

function App() {

  const [task, setTask] = useState({
    text: '',
    order: 1,
    id: uniqid()
  });
  const [tasks, setTasks] = useState([]);

  // order remains regardless of how much input changes
  // order changes its value only when form is submitted or an item deleted
  const inputChangeHandler = (e) =>{
    setTask((prevTask) => ({
      ...prevTask, 
      text: e.target.value
    }));
  } 

  const submitHandler = (e) => {
    e.preventDefault();
    // Avoid setTask right before setTasks whose value depends on Task !!!
    setTasks((prevTasks) => [...prevTasks, task]);
    setTask((prevTask) => ({
      text: '',
      order: prevTask.order + 1,
      id: uniqid()
    }))
  }

  const deleteHandler = (e) => {
    const id = e.target.parentNode.id;
    let deletedAt;
    // Remove target item
    let reducedList = tasks
      .filter((task, index) => {  
        if(task.id == id){
          deletedAt = index;
          return false;
        }
        return true;
      })
      .map((item, index) => {
        if(index >= deletedAt) return {...item, order: item.order -1};
        else return item;
      })
    
    // Update tasks
    setTasks([...reducedList]);

    // clear text field, decrease order after item deleted
    setTask({
      text: '',
      order: task.order - 1,
      id: uniqid()
    })
  }

  return (
      <>
          <form onSubmit={submitHandler}>
              <input type="text" id="taskInput" value={task.text} onChange={inputChangeHandler} placeholder="Create a task"></input>
              <button type="submit">Submit</button>
          </form>
          <Overview tasks={tasks} handleDelete={deleteHandler}/>
      </>
  )
}

export default App;

```
#### App breakdown
* Declaring a state variable
```jsx
  const [task, setTask] = useState({
    text: "",
    order: 0,
    id: uniqid()
  });
  const [tasks, setTasks] = useState([]);
```
`useState(initialValue)` returns a pair of value `[state, setState]`. initialValue can be anything, from a number, a string to an obj or an array. `setState` is an updater function. Here I declare `task` to manage a single to-do item data and `tasks` to keep track of many items.

* Reading state

In functional components, you can read a state directly:
```jsx
<input
          ...
          value={task.text}
></input>
```

* Updating state

As mentioned above,`setState` function to set or update a state, whatever returned by this function is set as a new state value.
`setState` has two forms. The first one is by passing a new value as an argument: `setState(newStateValue)`. Refer to line 65 where we update `tasks` array by passing in a new array:
```jsx
    let reducedList = tasks.filter(...)

    // Update tasks
    setTasks([...reducedList]);
```

**IMPORTANT NOTE 1**: State updates may be asynchronous. React may batch multiple setState() calls into a single update for performance. Therefore, never rely on state values to calculate the new, next state.

The first form of setState() works perfectly for most cases but in some cases, the new state value is calculated based on the previous value like a counter state, increase the old value by 1 whenever the button is clicked.

The following code may fail to update the task:
```jsx
// May fail to update
setTask({...task, text: ''});// update text, others unchanged
```

In our app, we update the input field whenever users press a key. Because we want `order` and `id` properties to be unchanged for every _onChange_ events. It means we're going to just update `task` partially instead of an entirely new state. In this circumstance, the second form of `setState()` comes in.

`setState((state, props) => newValue)` 

It accepts a function rather than an object. This function takes previous state as a first argument and props at the time when update is applied as second argument. Implement the second form to our handler:

```jsx
  const inputChangeHandler = (e) => {
    setTask((prevTask) => ({
      ...prevTask,
      text: e.target.value
    }));
  };
```
Use spread operator to keep those properties remained and specify which property to be set.

 `setTasks` works exactly the same as `setTask`:

```jsx
  const submitHandler = (e) => {
    e.preventDefault();
    // Avoid setTask right before setTasks whose value depends on Task's value !!!
    setTasks((prevTasks) => [...prevTasks, task]);
    setTask((prevTask) => ({
      text: '',
      order: prevTask.order + 1,
      id: uniqid()
    }))
  }
```

**IMPORTANT NOTE 2**: In React, state should be treated as immutable. Try to avoid to set state directly like state.order++ because it can lead to unexpected results or bugs. Instead, always use setState() updater function.

This note can be clearly illustrated by `deleteHandler` as below:
```jsx
  const deleteHandler = (e) => {
    const id = e.target.parentNode.id;
    let deletedAt;
    // Remove target item
    let reducedList = tasks
      .filter((task, index) => {  
        if(task.id == id){
          deletedAt = index;
          return false;
        }
        return true;
      })
      .map((item, index) => {
        if(index >= deletedAt) return {...item, order: item.order -1};
        else return item;
      })
    
    // Update tasks
    setTasks([...reducedList]);

    // clear text field, decrease order after item deleted
    setTask({
      text: '',
      order: task.order - 1,
      id: uniqid()
    })
  }
```
Just make a copy of `Tasks` so that we can make some modifications on this copy (remove item, update its value) on the side rather than set its state directly.
After construct an array of reduced, re-ordered to-do tasks, we now can use first form of `setState` to safely update `Tasks`


Never try to update `tasks` like this:
```jsx
setTasks((prevTasks) => {
  prevTasks.forEach((item, index) => {
    	if (index >= deletedAt){
          item.order -= 1; // You are changing state directly
        }
  })
})
```

### Overview component
```jsx
import React from "react";
import './Overview.css';

const Overview = (props) => {
  return (
    <ul className="task-list">
      {props.tasks.map((item) => {
        return (
          <li key={item.id} id={item.id}>
            <span>
              {item.order}. {item.text}
            </span>
            <button onClick={props.handleDelete}>X</button>
          </li>
        );
      })}
    </ul>
  );
};

export default Overview;
```
As you can see, we use `<ul>` to implement an ordered list. The order numbers get updated for every add/delete action. Here we use function map to dynamically render list item.

## CONCLUSION/TAKEAWAYS:

1. State should be treated as immutable. Never set the state directly like state.value++. Always rely on `setState` to manage state, avoid unexpected results and bugs.

2. State updates may be async. If your new state value is calculated based the old state, use the second form of `setState` where you pass in a function. If your new state value is independent from the previous state, feel free to use to first form of it `setState(newValue)`

 