const hamBurgerBtn = document.querySelector('.hamburger_btn');
const sideBox = document.querySelector('.side_box');
const sideBoxContent = document.querySelector('.side_box__content');
const sideBoxBackground = document.querySelector('.side_box__background');

const navBarSearch = document.querySelector('.navbar__search > form > input');
const navBarMobileSearch = document.querySelector('.navbar__search__mobile > div > form > input')

hamBurgerBtn.addEventListener('click', (e) => {
  // side-box
  sideBox.classList.remove('hidden');
  }
);

sideBoxBackground.addEventListener('click', (e) => {
  sideBox.classList.add('hidden');
})

// interrelated search fields
navBarSearch.addEventListener('change', (e) => {
  navBarMobileSearch.value = e.target.value;
});

navBarMobileSearch.addEventListener('change', (e) => {
  navBarSearch.value = e.target.value;
});
