$( document ).ready(function() {
	$( "select#searchcategoryType" ).hide();
	$( "select#searchgenre" ).hide();

	$( "#searchtype" ).change(function() {
		var selectBox = document.getElementById("searchtype");
		var selectedValue = selectBox.options[selectBox.selectedIndex].value;
		if(selectedValue == "category") {
			$( "select#searchcategoryType" ).show();
			$( "select#searchgenre" ).hide();
			$( "input#searchuserInput" ).hide();
			$( "span#iconsearch" ).hide();
		} 
		else if(selectedValue == "genre") {
			$( "select#searchgenre" ).show();
			$( "select#searchcategoryType" ).hide();
			$( "input#searchuserInput" ).hide();
			$( "span#iconsearch" ).hide();
		}
		else {
			$( "select#searchcategoryType" ).hide();
			$( "select#searchgenre" ).hide();
			$( "input#searchuserInput" ).show();
			$( "span#iconsearch" ).show();
		}
	});
});