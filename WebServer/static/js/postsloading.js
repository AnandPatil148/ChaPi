function displayPosts(data)
{
    var card = document.createElement("div");
    card.className= "card";
    
    //Title of the post
    var title = document.createElement("h5");
    //title.className=data[i].Name;
    title.setAttribute('class', 'title');
    title.innerHTML="By: "+data.Name;
    card.appendChild(title);
    
    //Post Message
    var message = document.createElement("p");
    message.setAttribute('class', 'message');
    message.innerHTML="Message: "+data.Message;
    card.appendChild(message);
    //Date and Time
    var time = document.createElement("small");
    time.setAttribute('class','time');
    time.innerHTML ="Time posted: "+ new Date(data.TimeStamp).toLocaleString(); 
    card.appendChild(time);
    
    //Adding a button to each card
    var btnShowMore = document.createElement("button");
    btnShowMore.className="btn btn-primary showmore";
    //btnShowMore.setAttribute('onclick','showComments(\''+data[i].Key+'\')');
    btnShowMore.innerHTML='Read more';
    card.appendChild(document.createTextNode("\u00A0"));//add some space
    card.appendChild(btnShowMore);
    
    // Append to body:
    document.getElementById("posts-display").appendChild(card);

}