### The 3 phases of a DOM Event
Trước đây biết lờ mờ, giờ mới đọc kĩ. Bất cứ 1 DOM event nào (click, input, change,...) đều có 3 phase là:

1. Capture: Giai đoạn event đc propagate từ container bên ngoài, đi dần vào target sâu nhất
2. Target: Khi event propagation kết thúc, và event object tới đc target element
3. Bubbling: Giai đoạn event đc propagate ngược từ target trở lên trên container ngoài cùng

Vì thế nên khi xài addEventListener thì thường xuất hiện tham số true hoặc false ở cuối, để bắt giai đoạn capture, full option của nó là addEventListener(..., { capture: true })
Khi handle event thì có thể biết đc đang ở phase nào thông qua giá trị event.eventPhase (có giá trị 1=capturing, 2=target, 3=bubbling) và event.currentTarget để biết đang ở target nào, khác với event.target luôn là target sâu nhất. Từ đó có tthểdùng event.stopPropagation() để dừng việc propagation ở bất kì giai đoạn nào tuỳ thích.

Trong React thì có những event handler như onChange và onChangeCapture.

Trên thực tế chỉ cần quan tâm đến giai đoạn bubbling, còn giai đoạn capture thì hầu như ít dùng.

![phases of a DOM event](/screenshots/dom-event-phase.png).



Source:

https://www.w3.org/TR/DOM-Level-3-Events/#dom-event-architecture

https://javascript.info/bubbling-and-capturing#capturing
