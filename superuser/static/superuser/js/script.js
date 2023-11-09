const findTotal = () => {
        const slots = document.getElementById('slots')
        const amount = document.getElementById('amount')
        
        const numericValue = Number(slots.value);

        if (isNaN(numericValue) || numericValue <= 0 ) {
            alert("Please enter a valid number");
            slots.value = ""
            amount.value = ""
        } else {
        //     amount.value = slots.value * 50
            if(slots.value == 10){
                amount.value = '400.00'

            } else if(slots.value == 20){
                amount.value = '750.00'
            } else {
                amt = slots.value * 50
                amount.value = `${amt}.00`
            }

        }
}




const getFile = () => {

        const signature = document.getElementById('signature')
        const signaturePreview = document.getElementById('signature-preview')
        const previewImage = document.querySelector(".image")
        const previewTextDefault = document.querySelector(".default-text")

        signature.addEventListener('change', function() {
                const file = this.files[0];
                
        
                if (file){

                        const reader = new FileReader()

                        previewTextDefault.style.display = "none"
                        previewImage.style.display = "block"
                        signaturePreview.style.border = "none"

                        reader.addEventListener('load', function() {
                                console.log(this.result)
                                previewImage.setAttribute("src", this.result)  
                        });

                        reader.readAsDataURL(file);

                }else{
                        previewTextDefault.style.display = null
                        previewImage.style.display = null   
                        signaturePreview.style.border = null
                        previewImage.setAttribute("src", "") 
                }
        })
}


const getLogo = () => {

        const logo = document.getElementById('logo')
        const logoPreview = document.getElementById('logo-preview')
        const previewImage = document.querySelector(".logo-image")
        const previewTextDefault = document.querySelector(".logo-text")

        logo.addEventListener('change', function() {
                const file = this.files[0];
                
                if (file){

                        const reader = new FileReader()

                        previewTextDefault.style.display = "none"
                        previewImage.style.display = "block"
                        logoPreview.style.border = "none"

                        reader.addEventListener('load', function() {
                                console.log(this.result)
                                previewImage.setAttribute("src", this.result)  
                        });

                        reader.readAsDataURL(file);

                }else{
                        previewTextDefault.style.display = null
                        previewImage.style.display = null   
                        logoPreview.style.border = null
                        previewImage.setAttribute("src", "") 
                }
        })
}







   