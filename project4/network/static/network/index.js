document.addEventListener("DOMContentLoaded", function() {});

// define function to edit the post
function editPost(postId, postContent){
    // hide edit button 
    document.querySelector(`#edit_button_${postId}`).style.display = 'none'
    
    const postVariable = document.getElementById(`post_content_${postId}`)
    postVariable.style.display = 'none'


    // create you wall where each post will loop 
    const wall = document.querySelector(`#single_post_${postId}`)

    // when button is clicked text area appears
    const textArea = document.createElement("textarea")

    // save button should appear next to text area
    saveButton = document.createElement("button")
    saveButton.textContent = "Save"
    // text area should display previous content
    textArea.textContent = postContent
    // save new content
    saveButton.addEventListener('click', function() {
        updatedContent = textArea.value

        fetch(`/edit_post/${postId}`, {
            method: "PUT",
            body:JSON.stringify({
                update: updatedContent
            })
        })

        .then(response => response.json())
        .then(result => {
            console.log(result)
        })
        // after save hide text area and save button and bring edit back
        textArea.style.display = 'none'
        saveButton.style.display = 'none'
        document.querySelector(`#edit_button_${postId}`).style.display = 'block'
        postVariable.textContent = updatedContent
        postVariable.style.display = 'block'
    })
   
    // display new content in all posts
    wall.append(textArea)
    wall.append(saveButton)
}

function likePost(postId){
    console.log("Like button clicked", postId)
    const like_btn = document.getElementById(`like_button_${postId}`)
    const unlike_btn = document.getElementById(`unlike_button_${postId}`)
    like_btn.style.display = 'none'
    unlike_btn.style.display = 'block'
    
    fetch(`/like/${postId}`, {
        // method is post because we are obtaining new information 
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        // body is the package/everything in our box 
        body: JSON.stringify({
            // can keep the body empty because we already have post ID with all info already inside 
        }) 
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
    })

}

function unlikePost(postId){
    console.log("unlike button clicked", postId)
    const unlike_btn = document.getElementById(`unlike_button_${postId}`)
    const like_btn = document.getElementById(`like_button_${postId}`)
    unlike_btn.style.display = 'none'
    like_btn.style.display = 'block'

    fetch(`/unlike/${postId}`, {
        method : "DELETE"
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
    })
    
}