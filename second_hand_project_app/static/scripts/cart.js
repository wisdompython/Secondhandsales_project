var CartButton = document.getElementsByClassName('update-cart')

for (i=0; i < CartButton.length; i++){
    CartButton[i].addEventListener('click', function(){
      // returns a product Id and an action
      var productId = this.dataset.product 
      var action = this.dataset.action
      if (user ==='AnonymousUser'){
        console.log('Please Login')
        console.log(productId)
      }
      else{
        UpdateUserOrder(productId,action)
      }
    })
}

function UpdateUserOrder(productId,action){
  // we will send data action in here

  var url=  '/update_cart/'
  fetch(url, {
    method:'POST',
    headers:{'Content-Type': 'application/json','X-CSRFToken': csrftoken},
    body : JSON.stringify({'productId':productId, 'action':action})

  })

  .then((response)=> {
    return response.json()
    
  })
  .then((data)=> {
    console.log('data:', data)
    location.reload()
    
  })

}