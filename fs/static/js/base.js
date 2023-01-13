console.log('================= from js/base.js ======================')
console.log('============= for Follow/Unfollow from base.js ===============')



// to popup a update card in myprofile page
$(document).ready(function() {
  $('#model-btn').click(function() {
    console.log('Working!');
    $('.ui.modal')
    .modal('show')
    ;
  })

  //dropdown menu in navbar firends 
  $('.ui.dropdown').dropdown()
})



// for deletions of notificitions 
$('#delete_all').submit(function(e){
  e.preventDefault()
  console.log("delete all notifications")
  $.ajax({
      type: 'POST',
      url: '/DeleteAllNotifications/',
      success: function(data) {
        if (data['deleted'] == true) {
          alert('All notifications deleted')
        }}
    })
})



// ===================================================================
// ======================== NOTIFICATIONS  ==========================
// ===================================================================

/* Anything that gets to the document
   will hide the dropdown */
// $(document).click(function(){
// $("#dropdown").show();
// });


/* Clicks within the dropdown won't make
//    it past the dropdown itself */
// $("#dropdown").click(function(e){
// e.stopPropagation();
// });
// // Delete a single notification
// $('.read_one').submit(function(e){
//   e.preventDefault()
//   console.log("read one notification *************")
//   var pk = $(this).attr('id')
//   var url = $(this).attr('action')

//   console.log("pk: " + pk)
//   console.log("url: " + url)
//   $.ajax({
//       type: 'POST',
//       url: url,
//       data: {
//         'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
//         'pk': pk,
//       },
//       success: function(data) {
//         if (data['success'] == true) {
//           $(`#noti_box`).hide("slow", "linear")
//           // alert('Notification Read')
//         }}
//     })
// })