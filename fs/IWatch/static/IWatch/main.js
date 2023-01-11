console.log("****************** from IWatch ***********888888888")
// =================================================================
// ========================= For Comments =========================
// =================================================================

$('.commentForm').submit(function(e){
e.preventDefault()

const post_id = $(this).attr('id')
const url = $(this).attr('action')
const commentField = document.getElementById('comment' + post_id);
console.log(commentField.value, '*************')

$.ajax({
    type: 'POST',
    url: '/IWatch/create_comment/',
    data: {
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        'post_id':post_id,
        'body': commentField.value,
    }, 
    success: function(data) {
        $(`.commentForm`)[0].reset();
        $(`#comment_total${post_id}`).html(data['no_of_comments']+ ' Comments')
        $(`#c_body${post_id}`).html(data['c_body'])
        $(`#c_user${post_id}`).html(data['c_user'])
        $(`#c_date${post_id}`).html(data['c_date'])
    }
})

// get comment if enter presss
$(document).ready(function() {
    $("#comment" + post_id).keypress(function(e) {
        if (e.which == 13) {
        var val = $("#comment" + post_id).val();
        // alert("send");
    }        
});
});

})


// =================================================================
// ========================= For Likes =========================
// =================================================================

$('.like-form').submit(function(e){
e.preventDefault()

const post_id = $(this).attr('id')
const url = $(this).attr('action')
console.log("*************** from Like form", post_id, url)
$.ajax({
    type: 'POST',
    url: url,
    data: {
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        'post_id':post_id,
    }, 
    success: function(data) {
        console.log(data['like'], '*************')
        if (parseInt(data['like']) > 0) {
            console.log(parseInt(data['like']), '*************')
            $(`.like-count${post_id}`).html(parseInt(data['like']))
        }
        else {
            $(`.like-count${post_id}`).html(0)
            console.log(parseInt(data['like']), '*************')
        }
    }
})
})


/// =================================================================
// ========================= Dislike Follow =========================
// =================================================================
