const likeicon = document.getElementById('like-icon')
const likecount = document.getElementById('like-count')

likeicon.onclick = () => {
    const blogId = likeicon.getAttribute('data-blog');
    const url =  `/likeblogs/${parseInt(blogId)}/`;
    fetch(url, {
        method: 'GET',
        headers: {
            'Content_type': 'applicatin/json'
        }
    })
    .then(response =>{
        return response.json();
    })
    .then(data => {
        if(data.liked){
            likeicon.classList.remove('empty-heart')
            
        }
        else {
            likeicon.classList.add('empty-heart')
        }
        likecount.innerHTML = data.like_count;
    })
    .catch(error =>{
        console.log(error)
    })
}
