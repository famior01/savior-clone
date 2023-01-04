// clicking on the upvote butto
console.log("================== from buttons.js ==================")
$('.upvote-form').submit(function(e){
e.preventDefault()

const post_id = $(this).attr('id')
const url = $(this).attr('action')

$.ajax({
    type: 'POST',
    url: url,
    data: {
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        'post_id':post_id,
    }, 
    success: function(data) {
        console.log(data['upvote'], '*************')
        if (parseInt(data['upvote']) > 0) {
            console.log(parseInt(data['upvote']), '*************')
            $(`.upvote-count${post_id}`).html(parseInt(data['upvote']))
        }
        else {
            $(`.upvote-count${post_id}`).html(0)
            console.log(parseInt(data['upvote']), '*************')
        }
    }
})
})



// downvote button
$('.downvote-form').submit(function(e){
    e.preventDefault()
    const post_id = $(this).attr('id')
    const url = $(this).attr('action')

    $.ajax({
    type: 'POST',
    url: url,
    data: {
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        'post_id':post_id,
    }, 
    success: function(data) {
        console.log(data['downvote'], '*************')
        if (parseInt(data['downvote']) > 0) {
            $(`.downvote-count${post_id}`).html(parseInt(data['downvote']))
            console.log(parseInt(data['downvote']), '*************')
        }
        else {
            $(`.downvote-count${post_id}`).html(0) // if the downvote is undefined, it will show 0
            console.log(parseInt(data['downvote']), '*************')
        }
    },
    })

})