document.addEventListener('DOMContentLoaded', () => {
  const item_count = document.querySelector('.item_count');
  const addToCartBtns = document.querySelectorAll('.add_to_cart_btn');

  const upBtns = document.querySelectorAll('.up_btn');
  const downBtns = document.querySelectorAll('.down_btn');
  const numbers = document.querySelectorAll('.number');
  const deleteBtns = document.querySelectorAll('.delete_btn');

  const total = document.querySelector('.total');
  const item_total_count = document.querySelector('.item_total_count');

  const availability = document.querySelectorAll('.cart_page .availability');

  const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  const csrftoken = getCookie('csrftoken');

  const getTotal = (isInCart) => {
    // fetch a request to /cart
    fetch('/cart')
      .then(res => res.json())
      .then(data => {
        if (data.status === 200) {
          if (data.item_count > 99) {
            data.item_count = "99+"
          }
          item_count.innerHTML = data.item_count;
          if (isInCart) {
            total.innerHTML = `$${data.total}`;
            if (data.item_count > 1) {
              item_total_count.innerHTML = `${data.item_count} items`;
            } else {
              item_total_count.innerHTML = `${data.item_count} item`;
            }
          }
        }
      })
      .catch(e => {
        console.log(e)
      })
  }

  const addToCart = (e, isInCart) => {
    let id = e.target.dataset.id;

    const formData = new FormData();
    formData.append("id", id);

    // fetch POST request to /cart/add_to_cart/
    fetch('/cart/add_to_cart/', {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': csrftoken
      }
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 200) {
          getTotal(isInCart);

          if (isInCart) {
            numbers.forEach(number => {
              if (number.dataset.id === id) {
                number.innerHTML = data.product_quantity
              }
            });

            if (data.product_quantity > 1) {
              downBtns.forEach(btn => {
                if (btn.dataset.id === e.target.dataset.id) {
                  btn.classList.remove('disabled');
                }
              });
            }

            if (data.item_stock <= 0) {
              availability.forEach(item => {
                if (item.dataset.id === e.target.dataset.id) {
                  item.innerHTML = 'Out Of Stock';
                  item.classList.remove('available');
                  item.classList.add('not_available');
                }
              });
              e.target.classList.add('disabled');
            }
          }

          if (data.item_stock <= 0) {
            e.target.disabled = true;
          }
        }
      })
      .catch(e => [
        console.log(e)
      ]);
  }

  const removeFromCart = (e) => {
    let id = e.target.dataset.id;

    numbers.forEach(number => {
      if (number.dataset.id === id) {
        if (parseInt(number.innerHTML) > 1) {

          const formData = new FormData();
          formData.append("id", id);

          // fetch POST request to /cart/add_to_cart/
          fetch('/cart/remove_from_cart/', {
            method: 'POST',
            body: formData,
            headers: {
              'X-CSRFToken': csrftoken
            }
          })
            .then(res => res.json())
            .then(data => {
              if (data.status === 200) {
                getTotal(true);

                numbers.forEach(number => {
                  if (number.dataset.id === id) {
                    if (data.product_quantity > 1) {
                      number.innerHTML = data.product_quantity;
                    } else if (data.product_quantity === 1) {
                      number.innerHTML = data.product_quantity;
                      e.target.classList.add('disabled');
                    }
                  }
                });

                if (data.item_stock > 0) {
                  availability.forEach(item => {
                    if (item.dataset.id === e.target.dataset.id) {
                      item.innerHTML = 'In Stock';
                      item.classList.remove('not_available');
                      item.classList.add('available');
                    }
                  })

                  upBtns.forEach(btn => {
                    if (btn.dataset.id === e.target.dataset.id) {
                      btn.classList.remove('disabled');
                    }
                  });
                }
              }
            })
            .catch(e => [
              console.log(e)
            ]);
        }
      }
    });
  }

  const removeCart = (e) => {
    let id = e.target.dataset.id;

    const formData = new FormData();
    formData.append("id", id);

    // fetch POST request to /cart/add_to_cart/
    fetch('/cart/remove_cart/', {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': csrftoken
      }
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 200) {
          window.location.reload();
        }
      })
      .catch(e => [
        console.log(e)
      ]);
  }

  addToCartBtns.forEach((btn) => {
    btn.addEventListener('click', function (e) {
      addToCart(e, false);
    })
  });

  upBtns.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      addToCart(e, true);
    })
  });

  downBtns.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      removeFromCart(e);
    })
  });

  deleteBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      removeCart(e);
    })
  });

  if (window.location.pathname == '/shopping_cart/') {
    getTotal(true);
  } else {
    getTotal();
  }
});
