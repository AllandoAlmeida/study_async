(function() {
  let cardOpen = null;
  window.flip_card = function(id) {
   
    let card = document.getElementById(id);

    if (card) {
      if (card.style.display === "none" || card.style.display === "") {
       
        if (cardOpen !== null && cardOpen !== card) {
          cardOpen.style.display = "none";
        }

     
        card.style.display = "block";
        cardOpen = card;
      } else {
       
        card.style.display = "none";
        cardOpen = null;
      }
    } else {
      console.error(`Elemento com ID '${id}' não encontrado.`);
    }
  };
})();
