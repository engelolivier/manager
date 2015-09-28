moment.locale('fr')

$.ajaxSetup({   headers: {  "X-CSRFToken": $.cookie('csrftoken')  }  });

app = angular.module 'app', ['ngRoute', 'ngResource', 'ui.sortable', 'dndLists']

$.fn.datetimepicker.dates['en'] = {
	days: ["Dimanche", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"],
	daysShort: ["Dim", "Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"],
	daysMin: ["D", "L", "Ma", "Me", "J", "V", "S", "D"],
	months: ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aot", "Septembre", "Octobre", "Novembre", "Décembre"],
	monthsShort: ["Jan", "Fev", "Mar", "Avr", "Mai", "Jui", "Jul", "Aou", "Sep", "Oct", "Nov", "Dec"],
	today: "Aujourd'hui",
	suffix: [],
	meridiem: ["matin", "aprem"],
	weekStart: 1,
	format : 'dd/mm/yyyy hh:ii',
	# minView : 'month',
	autoclose: true,
};

app.config ($routeProvider, $interpolateProvider, $httpProvider, $resourceProvider) ->
   
	# $httpProvider.interceptors.push 'httpInterceptor'
	$httpProvider.defaults.headers.common['X-CSRFToken'] = $.cookie('csrftoken')
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

	$interpolateProvider.startSymbol '~{'
	$interpolateProvider.endSymbol '}~'

	$httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
	# $httpProvider.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8";

	$resourceProvider.defaults.stripTrailingSlashes = false

	$routeProvider
	.when '/backlog', templateUrl: '/backlog', controller: 'BacklogController', title : 'Backlog'
	.when '/sprint', templateUrl: '/sprint', controller: 'SprintController', title : 'Sprint'
	.otherwise redirectTo: '/backlog'
	return


app.factory 'Task', [
  '$resource'
  ($resource) ->
    $resource '/api/task/:id',  {id: '@id'}, 
    	{
    	'update': { method: 'PUT', params: {id: '@id'} },
    	'query': {method: 'GET', isArray: false }
   		}
]

app.factory 'Sprint', [
  '$resource'
  ($resource) ->
    $resource '/api/sprint/:id',  {id: '@id'}, 
    	{
    	'update': { method: 'PUT', params: {id: '@id'} },
    	'query': {method: 'GET', isArray: false }
   		}
]

app.factory 'Employee', [
  '$resource'
  ($resource) ->
    $resource '/api/employee/:id',  {id: '@id'}, 
    	{
    	'update': { method: 'PUT', params: {id: '@id'} },
    	'query': {method: 'GET', isArray: false }
   		}
]

app.filter "get_utc_datetime", () ->
   return (date) ->
   		return get_utc_datetime(date)

app.filter "get_utc_date", () ->
   return (date) ->
   		return get_utc_date(date)


get_utc_datetime = (date) ->

	d = moment(date, moment.ISO_8601).utc()

	if d.isValid()
		return d.format("DD/MM/YYYY HH:mm")
	else
		return ""

get_utc_date = (date) ->

	d = moment(date, "YYYY-MM-DD")

	if d.isValid()
		return d.format("DD/MM/YYYY")
	else
		return ""

set_utc_datetime = (date) ->

	if date == "" or date == undefined
		return ""
	else
		return moment(date, "DD/MM/YYYY HH:mm").format("YYYY-MM-DDTHH:mm:ss") + "Z"

set_utc_date = (date) ->

	if date == "" or date == undefined
		return ""
	else
		return moment(date, "DD/MM/YYYY").format("YYYY-MM-DD")