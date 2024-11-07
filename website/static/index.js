function showCalendar(events)
{
//   var calendarEl = document.getElementById('aiCalendar');

//   events = [{
//     title: "Meeting Fire Alarm",
//     start: "2024-10-16T21:00:00",
//     end: "2024-10-16T22:00:00"
// }]

//   var newCalendar = new FullCalendar.Calendar(calendarEl, {
//     timeZone: 'local',
//     initialView: 'dayGridMonth',
//     themeSystem: 'bootstrap5',
//     weekNumbers: true,
//     dayMaxEvents: true,
//     headerToolbar: 
//     {
//       left: 'dayGridMonth timeGridWeek timeGridDay list',
//       center: 'title',
//       end: 'prev today next',
//     },
//     events: events,
//   });

//   console.log("hello world")
//   newCalendar.render();
     console.log(events)
}

function showForm()
{
  hideAll();
  let form = document.getElementById("eventForm");

  if (form.style.display === "block")
  {
    form.style.display = "none"
  }
  else
  {
    form.style.display = "block"
  }
}

function showDelete()
{
  hideAll();

  let form = document.getElementById("deleteForm");

  if (form.style.display === "block")
  {
    form.style.display = "none"
  }
  else
  {
    form.style.display = "block"
  }
}

function showAI()
{

  hideAll();

  let form = document.getElementById("aiForm");

  if (form.style.display === "block")
  {
    form.style.display = "none"
  }
  else
  {
    form.style.display = "block"
  }
}

function hideAll()
{
  let deleteForm = document.getElementById("deleteForm");
  let eventForm = document.getElementById("eventForm");
  let aiForm = document.getElementById("aiForm");

  deleteForm.style.display = "none"
  eventForm.style.display = "none"
  aiForm.style.display = "none"
}