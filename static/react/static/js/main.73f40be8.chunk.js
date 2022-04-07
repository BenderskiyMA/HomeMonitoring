(this["webpackJsonpsimple-react-2"]=this["webpackJsonpsimple-react-2"]||[]).push([[0],{180:function(e,t,n){},181:function(e,t,n){},182:function(e,t,n){},183:function(e,t,n){},184:function(e,t,n){},185:function(e,t,n){},292:function(e,t,n){},293:function(e,t,n){},294:function(e,t,n){"use strict";n.r(t);var s=n(1),o=n.n(s),r=n(86),a=n.n(r),i=(n(180),n(41)),c=n(42),l=n(46),u=n(45),d=(n(181),n(50)),h=(n(182),n(183),n(63)),m=n.n(h);function j(e){switch(e){case"%":return"%";case"volt":return"V";default:return"\xb0C"}}function b(e){switch(e){case"temp":return"\u0422\u0435\u043c\u043f\u0435\u0440\u0430\u0442\u0443\u0440\u0430";case"hum":return"\u0412\u043b\u0430\u0436\u043d\u043e\u0441\u0442\u044c";case"volt":return"\u041d\u0430\u043f\u0440\u044f\u0436\u0435\u043d\u0438\u0435";default:return"\u041d\u0435\u0438\u0437\u0432\u0435\u0441\u0442\u043d\u044b\u0439 \u0442\u0438\u043f"}}function f(e,t){return m()(Date.parse(e)).add(t,"h").toDate()}var v=n(169),p=(n(184),n(300)),O=n(302),g=n(158),x=n(303),N=(n(185),n(7)),y=function(e){Object(l.a)(n,e);var t=Object(u.a)(n);function n(e){var s;return Object(i.a)(this,n),(s=t.call(this,e)).getChartData=function(){var e;(s.setState(Object(d.a)(Object(d.a)({},s.state),{},{isFetching:!0})),null!=s.sensorId)?(e="http://home.remlo.ru:8081/api/data/"+s.sensorId+"/"+s.timeinterval,console.log(e),fetch(e,{headers:{"Content-Type":"application/json"}}).then((function(e){return e.json()})).then((function(e){return s.setState({Data:e,isFetching:!1})})).catch((function(e){return console.log(e)})),console.log(s.state.Data),console.log(s.state.isFetching)):console.log("Waiting for sensor...")},s.timer=null,s.sensorId=e.sensorId,s.sensorName=e.sensorName,s.sensorUnitName=e.sensorUnitName,s.sensor=e.sensor,s.timeinterval="hour",s.state={isFetching:!1,Data:[]},console.log("TempChart created"),s}return Object(c.a)(n,[{key:"componentDidMount",value:function(){var e=this;this.getChartData(),this.timer=setInterval((function(){return e.getChartData()}),6e4)}},{key:"componentWillUnmount",value:function(){clearInterval(this.timer)}},{key:"render",value:function(){var e,t=this;return"week"!==this.timeinterval&&"month"!==this.timeinterval||(e=Object(N.jsx)(p.a,{data:this.state.Data,interpolation:"natural",y:"value2",x:"moment",style:{data:{fill:"none",stroke:"red",opacity:.7},labels:{fontSize:10},parent:{border:"1px solid #ccc"},border:"1px solid #ccc"}})),Object(N.jsxs)("div",{className:"ChartHolder",children:[Object(N.jsx)("div",{children:this.sensorName}),Object(N.jsxs)("div",{children:[Object(N.jsx)("button",{className:"button",onClick:function(){t.setimeinterval("hour")},children:"Hour"}),Object(N.jsx)("button",{className:"button",onClick:function(){return t.setimeinterval("day")},children:"Day"}),Object(N.jsx)("button",{className:"button",onClick:function(){return t.setimeinterval("week")},children:"Week"}),Object(N.jsx)("button",{className:"button",onClick:function(){return t.setimeinterval("month")},children:"Month"})]}),Object(N.jsxs)(O.a,{domainPadding:{x:0,y:[35,35]},padding:{left:10,right:-10,top:10,bottom:80},theme:g.a.material,children:[Object(N.jsx)(p.a,{data:this.state.Data,interpolation:"natural",y:"value",x:"moment",style:{data:{fill:"none",stroke:"blue",opacity:.7},labels:{fontSize:10},parent:{border:"1px solid #ccc"},border:"1px solid #ccc"}}),e,Object(N.jsx)(x.a,{fixLabelOverlap:!0,tickFormat:function(e){return"hour"===t.timeinterval||"day"===t.timeinterval?"".concat(new Date(e).toLocaleTimeString(navigator.language,{hour:"2-digit",minute:"2-digit"})):"".concat(new Date(e).toLocaleDateString(navigator.language,{day:"2-digit",month:"2-digit"}))},style:{}}),Object(N.jsx)(x.a,{dependentAxis:!0,label:j(this.sensorUnitName),style:{axisLabel:{fontSize:20,padding:40},tickLabels:{fontSize:15,padding:5},grid:{stroke:function(e){return 0===e.tick?"red":"grey"}}}})]})]})}},{key:"setimeinterval",value:function(e){this.timeinterval=e,this.getChartData()}}]),n}(o.a.Component),k=(n(292),function(e){e.message;var t=e.isOpen,n=e.onClose,s=(e.children,e.sensorId),o=e.sensorName,r=e.sensor,i=e.sensorUnitName;return t?(console.log("Modalchart created."),console.log(s),a.a.createPortal(Object(N.jsxs)("div",{className:"modal",children:[Object(N.jsx)(y,{sensorId:s,sensorName:o,sensor:r,sensorUnitName:i}),Object(N.jsx)("button",{className:"ButtonLeftTop",onClick:n,children:"[X]"})]}),document.body)):null});var C=function(e){var t=e.setTimerMethod,n=e.unsetTimerMethod,o=e.sensorId,r=e.sensorName,a=e.sensorUnitName,i=Object(s.useState)(!1),c=Object(v.a)(i,2),l=c[0],u=c[1];return Object(N.jsxs)("div",{children:[Object(N.jsx)("button",{onClick:function(){u(!0),n()},children:"Chart"}),Object(N.jsx)(k,{message:"Hello World!",isOpen:l,sensorId:o,sensorName:r,sensorUnitName:a,onClose:function(){u(!1),t()}})]})},S=function(e){var t;return Object(N.jsxs)("div",{className:(t=f(e.sensor.lastGoodValueMoment,0),m()(t).add(1,"h")<m()(f(new Date(m.a.now()),0))?"sensor-item-red":"sensor-item"),children:[Object(N.jsx)("div",{className:"sensor-item__title",children:e.sensor.sensorName}),Object(N.jsxs)("div",{children:[Object(N.jsxs)("p",{children:[e.sensor.lastGoodValue,j(e.sensor.sensorUnitName)]}),Object(N.jsx)("p",{children:f(e.sensor.lastGoodValueMoment,0).toLocaleString()}),Object(N.jsx)("p",{children:e.sensor.locationName}),Object(N.jsx)("p",{children:e.sensor.sensorId}),Object(N.jsx)("p",{children:b(e.sensor.sensorType)})]}),Object(N.jsx)("div",{className:"container-center",children:Object(N.jsx)(C,{setTimerMethod:function(){e.setTimerMethod()},unsetTimerMethod:function(){e.unsetTimerMethod()},sensorId:e.sensor.id,sensorName:e.sensor.sensorName,sensor:e.sensor,sensorUnitName:e.sensor.sensorUnitName})})]})};n(293);var D=function(e){return Object(N.jsx)("header",{className:"header",children:e})},T=function(e){Object(l.a)(n,e);var t=Object(u.a)(n);function n(e){var s;return Object(i.a)(this,n),(s=t.call(this,e)).startFetch=function(){s.fetchSensors(),s.timer=setInterval((function(){return s.fetchSensors()}),6e4),console.log("main timer started")},s.unsetTimer=function(){clearInterval(s.timer),console.log("main timer stopped")},s.fetchSensors=function(){s.setState(Object(d.a)(Object(d.a)({},s.state),{},{isFetching:!0})),fetch("http://home.remlo.ru:8081/api/sensors",{headers:{"Content-Type":"application/json"}}).then((function(e){return e.json()})).then((function(e){return s.setState({Sensors:e,isFetching:!1})})).catch((function(e){return console.log(e)})),console.log("log")},s.timer=null,s.state={isFetching:!1,Sensors:[]},console.log("sensorList created."),s}return Object(c.a)(n,[{key:"render",value:function(){var e=this;return Object(N.jsxs)("div",{className:"container-center",children:[Object(N.jsx)("div",{children:D("\u041c\u043e\u0438 \u0434\u0430\u0442\u0447\u0438\u043a\u0438")}),Object(N.jsx)("div",{className:"container",children:this.state.isFetching?"Fetching Sensors...":this.state.Sensors.map((function(t){return Object(N.jsx)(S,{setTimerMethod:e.startFetch,unsetTimerMethod:e.unsetTimer,sensor:t},t.id)}))})]})}},{key:"componentDidMount",value:function(){this.startFetch()}},{key:"componentWillUnmount",value:function(){this.unsetTimer()}}]),n}(s.Component),I=function(e){Object(l.a)(n,e);var t=Object(u.a)(n);function n(){return Object(i.a)(this,n),t.apply(this,arguments)}return Object(c.a)(n,[{key:"render",value:function(){return Object(N.jsx)("div",{className:"App",children:Object(N.jsx)(T,{id:"SensorList"})})}}]),n}(s.Component),M=I;a.a.render(Object(N.jsx)(o.a.StrictMode,{children:Object(N.jsx)(M,{})}),document.getElementById("root"))}},[[294,1,2]]]);
//# sourceMappingURL=main.73f40be8.chunk.js.map