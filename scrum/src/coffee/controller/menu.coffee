class MenuController

	@$inject: ['$scope', '$location'] 

	constructor: (@scope, $location) ->

		@scope.logout = @logout

		@scope.$on('loaderShow',  () =>

			@scope.showLoader = true
			true
		)
 
		@scope.$on('loaderHide', () =>

			@scope.showLoader = false
			true
		)

		@scope.menu_is_active = (route) =>
			return route == $location.path()
    
	logout : () =>
		if window.confirm "Êtes-vous sûr de vouloir quitter le site?"
			window.location = "/logout"

app.controller 'MenuController', MenuController