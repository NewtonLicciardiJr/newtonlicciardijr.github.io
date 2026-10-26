/** Drones — Muito Além do Voo. Private preparation environment.
 * Master source belongs in GitHub; account-specific values belong in Script Properties.
 * No learner enrollment, assessment or certificate issuance is enabled by this bootstrap.
 */
var COURSE_RULES = Object.freeze({hours:30,lessonCount:17,questionCount:20,passScore:70,maxAttempts:3,windowSeconds:7200});
var COURSE_SCHEMA = Object.freeze({
  Participants:['id','email','full_name','preferred_name','birth_date','created_at','consent_at','status'],
  LessonProgress:['participant_id','lesson_id','intervals_json','watched_seconds','completed_at','updated_at'],
  Attempts:['id','participant_id','cycle','started_at','deadline','submitted_at','status','score','questions_json','answers_json'],
  Documents:['id','participant_id','private_file_id','kind','status','reviewed_by','reviewed_at'],
  Certificates:['id','participant_id','private_file_id','issued_at','issued_by','authorization_reference'],
  TeacherReviews:['id','question_id','reviewer','status','note','updated_at'],
  Audit:['id','actor','action','target','at','detail_json'],
  CourseSettings:['key','value']
});

function ownerContext_(){
  var props=PropertiesService.getScriptProperties();
  var expected=String(props.getProperty('OWNER_EMAIL')||'').trim().toLowerCase();
  var actual=String(Session.getActiveUser().getEmail()||'').trim().toLowerCase();
  if(!expected||!actual||actual!==expected)throw new Error('Acesso restrito ao proprietário configurado.');
  return {props:props,email:actual};
}

/** Run manually in the editor, as the owner, after reviewing Google permissions. */
function setupProject(){
  var owner=ownerContext_();
  var lock=LockService.getScriptLock();lock.waitLock(30000);
  try{
    var rootId=owner.props.getProperty('COURSE_FOLDER_ID');
    if(!rootId)throw new Error('Configure COURSE_FOLDER_ID nas propriedades do script.');
    var root=DriveApp.getFolderById(rootId);
    var sheetId=owner.props.getProperty('COURSE_SHEET_ID');
    var book;
    if(sheetId){book=SpreadsheetApp.openById(sheetId);}
    else{
      book=SpreadsheetApp.create('Drones — registros privados do curso');
      owner.props.setProperty('COURSE_SHEET_ID',book.getId());
      DriveApp.getFileById(book.getId()).moveTo(root);
    }
    Object.keys(COURSE_SCHEMA).forEach(function(name){
      var sheet=book.getSheetByName(name)||book.insertSheet(name);
      if(sheet.getLastRow()===0){
        sheet.getRange(1,1,1,COURSE_SCHEMA[name].length).setValues([COURSE_SCHEMA[name]]);
        sheet.setFrozenRows(1);
      }else{
        var actual=sheet.getRange(1,1,1,COURSE_SCHEMA[name].length).getValues()[0];
        if(JSON.stringify(actual)!==JSON.stringify(COURSE_SCHEMA[name]))throw new Error('Estrutura existente incompatível: '+name+'. Nenhuma linha foi sobrescrita.');
      }
    });
    var settings=book.getSheetByName('CourseSettings');
    if(settings.getLastRow()===1){
      var values=Object.keys(COURSE_RULES).map(function(k){return [k,String(COURSE_RULES[k])];});
      values.push(['enrollmentEnabled','false'],['templateApproved','false'],['extensionApprovalReference','']);
      settings.getRange(2,1,values.length,2).setValues(values);
    }
    SpreadsheetApp.flush();
    owner.props.setProperty('COURSE_STAGE','storage_prepared');
    return projectStatus_();
  }finally{lock.releaseLock();}
}

function projectStatus(){ownerContext_();return projectStatus_();}
function projectStatus_(){
  var props=PropertiesService.getScriptProperties();
  return {stage:props.getProperty('COURSE_STAGE')||'awaiting_setup',storageConfigured:!!props.getProperty('COURSE_SHEET_ID'),enrollmentEnabled:false,assessmentEnabled:false,certificateIssuanceEnabled:false,hours:COURSE_RULES.hours,lessons:COURSE_RULES.lessonCount,videoHosting:'YouTube',master:'GitHub'};
}

function doGet(){
  try{
    ownerContext_();var status=projectStatus_();
    var html='<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Drones · preparação da plataforma</title><style>body{font:18px system-ui;margin:0;background:#f5f6f1;color:#10333b}main{max-width:900px;margin:8vh auto;padding:32px}small{color:#536a69}a{color:#084f60}h1{font-size:44px}section{background:white;padding:28px;border-radius:18px;border-top:5px solid #e60029}li{margin:12px 0}</style></head><body><main><small>DRONES — MUITO ALÉM DO VOO</small><h1>Preparação da plataforma Google.</h1><section><p>Vídeos mantidos no YouTube. Código mestre mantido no GitHub.</p><ul><li>Carga horária: 30 h/a.</li><li>Trilha: 17 aulas.</li><li>Registros privados: '+(status.storageConfigured?'estrutura preparada':'aguardando configuração')+'.</li></ul><p>Cadastro, avaliação e emissão ainda não foram migrados nem liberados neste ambiente.</p><p><a href="https://newtonlicciardijr.github.io/drones/" target="_top">Abrir portal do curso →</a></p></section></main></body></html>';
    return HtmlService.createHtmlOutput(html).setTitle('Drones — preparação da plataforma');
  }catch(error){
    return HtmlService.createHtmlOutput('<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Acesso restrito</title><p>Acesso restrito ao proprietário.</p></html>');
  }
}

function doPost(){throw new Error('Cadastro e avaliação ainda não foram habilitados neste ambiente.');}
