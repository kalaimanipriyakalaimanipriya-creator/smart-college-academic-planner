
var clearData, showData = ['Academic Excellence', 'Women Empowerment', 'Future Women Leaders'], index = 0;
let userData = { userType: '', userLoginType: '' }
var animateData = () => {
    let elementCreate = document.createElement('div');
    elementCreate.classList.add("class_o");
    elementCreate.style.opacity = 0;
    elementCreate.innerHTML = showData[index];
    document.querySelector(".parent_o").append(elementCreate);
    var i = 0;
    clearData = setInterval(async () => {
        var data = i / 4;
        let oldCss = document.querySelectorAll(".class_o")[0];
        oldCss.style.transform = `translateY(${data}px)`;
        oldCss.style.opacity = `${Math.abs(55 / data)}`;
        let newCss = document.querySelectorAll(".class_o")[1];
        newCss.style.transform = `translateY(${data}px)`;
        newCss.style.opacity = `${Math.abs(data / 55)}`;
        i -= 5;
        if (data == -55) {
            oldCss.remove();
            newCss.style.transform = `translateY(0px)`;
            newCss.style.opacity = `1`;
            index++;
            if (showData.length - 1 < index) {
                index = 0
            }
            clearInterval(clearData);
            await sleep(1500);
            animateData()
        }
    }
        , 5)
}

var sleep = (delay) => {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(true);
        }
            , delay);
    }
    );
}

var swiper = new Swiper(".swiper", {
    slidesPerView: 3,
    spaceBetween: 30,
    centeredSlides: true,
    grabCursor: true,
    loop: true,
    autoplay: {
        delay: 2500,
        disableOnInteraction: false,
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    on: {
        init: function () {
            $('.swiper-slide-prev').addClass('noScale')
            $('.swiper-slide-next').addClass('noScale')
            $('.swiper-slide-active').addClass('scale')
        },
        slideChangeTransitionStart: function () {
            $('.swiper-slide').removeClass('scale')
            $('.swiper-slide-prev').addClass('noScale')
            $('.swiper-slide-next').addClass('noScale')
            $('.swiper-slide-active').addClass('scale')
        },
    },
});

function loginClick(user) {
    userData.userLoginType = user;
    $('.modal-title').text('Select Your Role')
    $('.chooseUser').show().addClass('d-flex');
    $('.registerModal').hide();
    $('.loginModal').hide();
    (user == 'signup') ? $('#adminLogin').hide() : $('#adminLogin').show();
}

document.getElementById('studentLogin').addEventListener("click", function () {
    userData.userType = 'student'
    $('.chooseUser').hide().removeClass('d-flex');
    if (userData.userLoginType == 'login') {
        $('.modal-title').text('LOGIN')
        $('.registerModal').hide();
        $('.regNoParent').show();
        $('.userNameParent').hide();
        $('.loginModal').show();
    } else if (userData.userLoginType == 'signup') {
        $('.modal-title').text('REGISTER')
        $('.loginModal').hide();
        $('.designation').hide();
        $('.registerNumber').show();
        $('.registerModal').show();
    }
});

document.getElementById('staffLogin').addEventListener("click", function () {
    userData.userType = 'staff'
    $('.chooseUser').hide().removeClass('d-flex');
    if (userData.userLoginType == 'login') {
        $('.modal-title').text('LOGIN')
        $('.registerModal').hide();
        $('.regNoParent').hide();
        $('.userNameParent').show();
        $('.loginModal').show();
    } else if (userData.userLoginType == 'signup') {
        $('.modal-title').text('REGISTER')
        $('.loginModal').hide();
        $('.designation').show();
        $('.registerNumber').hide();
        $('.registerModal').show();
    }
});

document.getElementById('adminLogin').addEventListener("click", function () {
    userData.userType = 'admin'
    $('.chooseUser').hide().removeClass('d-flex');
    if (userData.userLoginType == 'login') {
        $('.modal-title').text('LOGIN')
        $('.registerModal').hide();
        $('.regNoParent').hide();
        $('.userNameParent').show();
        $('.loginModal').show();
    } else if (userData.userLoginType == 'signup') {
        $('.modal-title').text('REGISTER')
        $('.loginModal').hide();
        $('.registerModal').show();
    }
});

document.getElementById('loginForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const userName = $('.usernameLogin').val();
    const regNo = $('.regnoLogin').val();
    const Password = $('.passwordLogin').val();
    userData.userType = userData.userType == 'staff' ? 'staff' : regNo

    fetch("/login",{
        method:"POST",
        headers: {
            "Content-Type":"application/json"
        },
        body: JSON.stringify({
            password: Password,            
            userName: userName ? userName : '',
            regNo: regNo ? regNo : '',
            userType: userData.userType
        })
    }).then(res => res.json()).then(data => {
            let location = window.location.origin + '/dashboard'
            if(data.success) window.location.href = location 
        })
})

document.getElementById('registerForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const fullName = $('.fullnameRegister').val();
    const password = $('.passwordRegister').val();
    const email    = $('.emailRegister').val();

    const department  = $('.departmentRegister').val();
    const userName    = $('.userNameRegister').val();
    const designation = $('.designationRegister').val();
    const regNo = $('.regNo').val();

    userData.userType = userData.userType == 'staff' ? 'staff' : regNo
    fetch("/register",{
        method:"POST",
        headers: {
            "Content-Type":"application/json"
        },
        body: JSON.stringify({
            fullName: fullName,
            password: password,
            email: email,
            department: department,
            userName: userName,
            // regNo: regNo ? regNo : '',
            designation: designation ? designation : '',
            userType: userData.userType
        })
    }).then(res => res.json()).then(data => {
            let location = window.location.origin + '/academic-planner/home'
            if(data.success)
                alert('user registration success, please login')
                window.location.href = location
        })

})

animateData();