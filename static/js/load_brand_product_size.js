const brandName = document.getElementById('brand_name')
var productName = document.getElementById('product_name')
var productSize = document.getElementById('product_size')

brandName.addEventListener('change', e=>{
    const selectedValue = e.target.value
    $.ajax({
        type: 'GET',
        url: `product-json/${selectedValue}/`,
        success: function(response){
            const data = response.data
            productName.options.length = 0;
            productSize.options.length = 0;
	    var blankOptName = document.createElement('option')
	    blankOptName.text = " "
	    blankOptName.value = " "
	    productName.appendChild(blankOptName)
	    var blankOptSize = document.createElement('option')
	    blankOptSize.text = " "
	    blankOptSize.value = " "
	    productSize.appendChild(blankOptSize)
            var uniqProductName = []
            data.map(i=>{
                var optName = document.createElement('option')
                optName.text = i.name
                optName.value = i.name
		f = uniqProductName.indexOf(i.name)
		if (f < 0) {
                   productName.appendChild(optName)
       		   }
                var optSize = document.createElement('option')
                optSize.text = i.size
                optSize.value = i.size
                productSize.appendChild(optSize)
		uniqProductName.push(i.name)
            })
        },
        error: function(error){
            console.log(error)
        }
    })
})
