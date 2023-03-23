const openBtnMenu = document.querySelector('.js-menu-open');
const mobileMenu = document.querySelector('.js-menu-body')
const pages = document.querySelectorAll('.header__item a');
const header = document.querySelector('.header');
const currentPage = window.location.href;


if (openBtnMenu) {
    openBtnMenu.addEventListener("click", () => {
        mobileMenu.classList.toggle('is-open');
        openBtnMenu.classList.toggle('close');
    })
}

if (window.matchMedia('(min-width: 768px)').matches && mobileMenu.classList.contains('.is-open')) {
    mobileMenu.classList.remove('.is-open');
}

const hightlightPage = () => {
    pages.forEach(page => {
        if (currentPage.endsWith(page.href)) {
            page.parentElement.classList.add('current')
        }
    })
}

window.addEventListener("load", hightlightPage)

window.addEventListener("load", () => {
    if (currentPage.endsWith('/')) {
        header.classList.add('home');
        document.querySelector('.footer').classList.add('home');
    }
})

// * description to item
const descrBtn = document.querySelector('.js-descr-open');
const itemDescription = document.querySelector('.item-descr');

if (descrBtn) {
    descrBtn.addEventListener("click", () => {
        descrBtn.classList.toggle('shown');
        itemDescription.classList.toggle('shown');
        if (window.matchMedia('(max-width: 1024px)').matches) {
            document.body.classList.toggle('lock')
        }
    });
}

// const deleteBtns = document.querySelectorAll('.manage__btn--delete');

// if (deleteBtns.length !== 0) {
//     for (const deleteBtn of deleteBtns) {
//         deleteBtn.addEventListener("click", () => {
//             const confirmDelete = confirm("Are you sure?");
//             if (confirmDelete === true) {

//             }
//         })
//     }
// }
