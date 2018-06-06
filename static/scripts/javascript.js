function positiveSelection()
{
  var textComponent = document.getElementById('Editor');
  var selectedText;



  if (textComponent.selectionStart !== undefined)
  {// Standards Compliant Version
    var startPos = textComponent.selectionStart;
    var endPos = textComponent.selectionEnd;
    selectedText = textComponent.value.substring(startPos, endPos);
  }
  else if (document.selection !== undefined)
  {// IE Version
    textComponent.focus();
    var sel = document.selection.createRange();
    selectedText = sel.text;
  }


  $.get("/getmethod/"+selectedText);
}

function printExamples(){
  $.get("/getexamples");
}

function sayHello(){
  alert("Hello world!");
}