function PositiveSelection()
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

  alert("Positive example: " + selectedText);
}


function NegativeSelection()
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

  alert("Negative example: " + selectedText);
}


function sayHello(){
  alert("Hello world!");
}