
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
<script type="text/javascript">
    $(function () {
        $("#chkShowPassword").bind("click", function () {
            var txtPassword = $("#txtPassword");
            if ($(this).is(":checked")) {
                txtPassword.after('<input onchange = "PasswordChanged(this);" id = "txt_' + txtPassword.attr("id") + '" type = "text" value = "' + txtPassword.val() + '" />');
                txtPassword.hide();
            } else {
                txtPassword.val(txtPassword.next().val());
                txtPassword.next().remove();
                txtPassword.show();
            }
        });
    });
    function PasswordChanged(txt) {
        $(txt).prev().val($(txt).val());
    }
</script>