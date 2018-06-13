function positiveSelectionTrain()
{
  var textComponent = document.getElementById('trainEditor');
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


  $.get("/addTextTrain/"+selectedText);
}

function positiveSelectionTest()
{
  var textComponent = document.getElementById('testEditor');
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


  $.get("/addTextTest/"+selectedText);
}


function Learn(){
  $.get("/learn");
}

function Test(){
  $.get("/test")
}