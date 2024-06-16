const btns = document.getElementsByClassName("btn-like");
console.log(btns);
Array.from(btns).forEach((btn)=>{
    btn.addEventListener("click",(e)=>{
        const pk=btn.getAttribute("data-like");
        console.log(pk);
        console.log('btn-like-clicked');
        fetch(`likes/${pk}/`, {method:"GET"})
            .then((res)=>{
                btn.classList.toggle("btn-like-active");
                btn.classList.toggle("btn-like-inactive");
            })
    });
});