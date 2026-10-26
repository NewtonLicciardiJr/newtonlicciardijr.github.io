import vm from 'node:vm';import fs from 'node:fs';import assert from 'node:assert/strict';
const code=fs.readFileSync(new URL('./Code.gs',import.meta.url),'utf8');
const lessons=JSON.parse(fs.readFileSync(new URL('./lessons-public.json',import.meta.url),'utf8'));
let count=0;const check=(ok)=>{assert.ok(ok);count++;};
check(lessons.length===17&&lessons.every(x=>/^[\w-]{11}$/.test(x.youtubeId)));
check(!/chatgpt|openai|password|secret|oauthToken/i.test(code));
let active='owner@example.test',creates=0,moves=0,locks=0,unlocks=0;
const properties=new Map([['OWNER_EMAIL',active],['COURSE_FOLDER_ID','private-test-folder']]);
const books=new Map();
function sheet(name){
 const rows=[];
 return {name,rows,getLastRow(){return rows.length;},setFrozenRows(){},
  getRange(r,c,h,w){
   return {
    setValues(values){for(let i=0;i<h;i++)rows[r-1+i]=[...values[i]];return this;},
    getValues(){return rows.slice(r-1,r-1+h).map(x=>x.slice(c-1,c-1+w));}
   };
  }
 };
}

const env={PropertiesService:{getScriptProperties(){return {getProperty:k=>properties.get(k)||null,setProperty(k,v){properties.set(k,String(v));return this}}}},Session:{getActiveUser(){return {getEmail:()=>active}}},LockService:{getScriptLock(){return {waitLock(){locks++},releaseLock(){unlocks++}}}},DriveApp:{getFolderById(id){assert.equal(id,'private-test-folder');return {id}},getFileById(){return {moveTo(){moves++}}}},SpreadsheetApp:{create(){creates++;const tabs=new Map();const b={getId:()=>`sheet-${creates}`,getSheetByName:n=>tabs.get(n),insertSheet(n){const s=sheet(n);tabs.set(n,s);return s},tabs};books.set(b.getId(),b);return b},openById(id){return books.get(id)},flush(){}},HtmlService:{createHtmlOutput(html){return {html,setTitle(){return this}}}}};
vm.createContext(env);vm.runInContext(code,env);
let result=env.setupProject();check(result.storageConfigured&&!result.enrollmentEnabled&&!result.assessmentEnabled&&!result.certificateIssuanceEnabled);
check(creates===1&&moves===1&&books.get('sheet-1').tabs.size===8);
env.setupProject();check(creates===1&&books.get('sheet-1').tabs.get('CourseSettings').rows.length===10);
check(locks===unlocks);
active='visitor@example.test';assert.throws(()=>env.setupProject(),/restrito/);check(creates===1);assert.throws(()=>env.projectStatus(),/restrito/);check(env.doGet().html.includes('restrito'));
active='';assert.throws(()=>env.setupProject(),/restrito/);check(creates===1);
active='owner@example.test';books.get('sheet-1').tabs.get('Participants').rows[0][0]='incompatible';assert.throws(()=>env.setupProject(),/incompatível/);check(creates===1&&locks===unlocks);
assert.throws(()=>env.doPost(),/não foram habilitados/);check(true);
check(env.doGet().html.includes('não foram migrados'));
console.log(JSON.stringify({passed:count,realGoogleDataTouched:false,source:'Code.gs'}));
