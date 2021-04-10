function rate(target_url, id_user, id_house, token){
    $.ajax({
      url: target_url,
      data: JSON.stringify({ id_user, id_house }),
      type: 'POST',
      headers: {
        "X-CSRFToken": token,
      },
      contentType: "application/json",
      dataType: "json",
      success: function (response) {
        for (let index = 0; index < document.getElementsByClassName("likes-house-"+id_house).length; index++) {
          document.getElementsByClassName("likes-house-"+id_house)[index].innerHTML = response["likes"].likes + " ";
          document.getElementsByClassName("dislikes-house-"+id_house)[index].innerHTML = response["dislikes"].dislikes + " ";
          var house_stars = document.getElementsByClassName("house-"+id_house+"-stars")[index];
          house_stars.innerHTML = "";
          if(response["stars"] == null){
            house_stars.innerHTML = 'Sin valoración<i class="fas fa-star" style="color: transparent;"></i>';
          }
          else{
            for (let star = 1; star <= response["stars"]; star++){
              house_stars.innerHTML = house_stars.innerHTML + '<i class="fas fa-star"></i> ';
            }  
          }
        }
      },
      error: function (error) {
        console.log(error);
      }
    });
}

function add_to_fav(target_url, id_user, id_house, token){
  $.ajax({
    url: target_url,
    data: JSON.stringify({ id_user, id_house }),
    type: 'POST',
    headers: {
      "X-CSRFToken": token,
    },
    contentType: "application/json",
    dataType: "json",
    success: function (response) {
      if (response["text"] == "added") {
        document.getElementById("btn-fav").innerHTML = '<i style="margin: 5px;" class="fas fa-star"></i>Eliminar de favoritos';
      }
      else {
        document.getElementById("btn-fav").innerHTML = '<i style="margin: 5px;" class="fas fa-star"></i>Añadir a favoritos';
      }
        
    },
    error: function (error) {
      console.log(error);
    }
  });
}


function add_to_fav_from_block(target_url, id_user, id_house, token){
  $.ajax({
    url: target_url,
    data: JSON.stringify({ id_user, id_house }),
    type: 'POST',
    headers: {
      "X-CSRFToken": token,
    },
    contentType: "application/json",
    dataType: "json",
    success: function (response) {
      var elements = document.getElementsByClassName("btn-fav-house-"+id_house);
      if (response["text"] == "added") {
        for (let index = 0; index < elements.length; index++) {
          elements[index].innerHTML = '<i style="font-size: 25px; margin: 5px;" class="fas fa-star"></i>';
        }
      }
      else {
        for (let index = 0; index < elements.length; index++) {
          elements[index].innerHTML = '<i style="font-size: 25px; margin: 5px; color: white;" class="fas fa-star"></i>';
        }
      }
        
    },
    error: function (error) {
      console.log(error);
    }
  });
}