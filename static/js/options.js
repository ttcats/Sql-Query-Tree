// 是否禁用
function isDisable()
{
    return confirm('确定禁用该条配置？');
}

// 是否启用
function isEnable()
{
    return confirm('确定启用该条配置？');
}

// 是否删除
function isDel()
{
    return confirm('确定删除该条配置？');
    //var a=confirm('确定删除该条配置？');
    //if (a == true)
    //{document.write("恭喜你答对了！")}
}

// 新增
function AddOps() {
	//document.getElementById("AddTr").style.display = "none"; 
    document.getElementById("AddTr").style.display = "table-row";
}

function AddSelect() {
	//document.getElementById("AddTr").style.display = "none"; 
    document.getElementById("AddSelect").style.display = "inline";
    document.getElementById("AddInput").style.display = "inline";
}

// 取消新增
function CancellNullOps() {
	document.getElementById("AddTr").style.display = "none"; 
    //document.getElementById("AddTr").style.display = "inline";
}

// 重置表单
function ResetForm(FormID) {
	document.getElementById(FormID).reset();
	document.getElementById('AddType').focus();
	
}

// 提交新增
function SubmitOps() {
	document.AddForm.submit();
}

// 编辑模式与取消编辑模式
function EditOps(ShowID,HideID) {
	document.getElementById(HideID).style.display = "none"; 
    document.getElementById(ShowID).style.display = "table-row";
}

// 保存编辑后的结果
function SaveOps(FormID) {
    document.getElementById(FormID).submit();
}

// 删除表单
function DelOps(FormID) {
    var a=confirm('确定删除该条配置？');
    if (a == true)
    {removeObj.parentNode.removeChild(FormID);}
}


function Delops(FormID) {
    var a=confirm('确定删除该条配置？');
    if (a == true)
    {var xmlhttp;
    xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange=function()
    {
    if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
        document.getElementById("myDiv").innerHTML=xmlhttp.responseText;
        }
    }
    xmlhttp.open("GET",FormID,true);
    xmlhttp.send();
    window.location.reload();
    }
}


function onSearches(selectID,row){
	$.ajax({
	type:"get",
	url:"/options",
        async:true,
        data:{selid:$("#show4type").val()},
        sucess:function(msg){
	alert("true");},
});
}
