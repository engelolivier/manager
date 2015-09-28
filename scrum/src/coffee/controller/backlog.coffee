class BacklogController

	@$inject: ['$scope', '$rootScope', 'Task', 'Employee', '$http' ] 

	constructor: (@scope, $rootScope, Task, $http) ->

		@Task                    = Task
		@http                    = $http
		@rootScope               = $rootScope
		@scope.tasks             = @get_tasks()
		@scope.run_modal         = @run_modal
		@scope.run_action        = @run_action
		@scope.modal_task        = @modal_task
		@scope.$on("task_recorded", () =>
			@get_tasks()
		)
		@scope.sortableOptions = stop: (e, ui) =>
			new_index = ui.item.index()
			task = @scope.tasks[new_index]
			positions = []
			for task, i in @scope.tasks
				positions.push task.id
			$.post(
				"/task/change_priority/" + task.id, 
				{'positions':positions.join(":")},
				(r) =>
					@get_tasks()
					alertify.success("Changement de priorité effectué avec succès")
					true
			)
			true
		true

	modal_task: (task) =>

		@rootScope.$broadcast('modal_task', task or {})
		true

	run_action: (action) =>

		tasks_selected = @get_tasks_selected()
		if tasks_selected.length == 0
			alertify.alert "Veuillez sélectionner des tâches"
			return true
		data = {
			'ids': (item.id for item in tasks_selected).join(':'), 
			'action': action
		}
		if action == "sprint_prompt"
			$('#modal_run_action_options').modal 'show'
			return true
		else if action == "sprint"
			data.sprint = @scope.run_action_option.sprint
		else if action == "delete_confirm"
			alertify.confirm "Êtes-vous sur de vouloir supprimer les tâches sélectionnées?", () =>
				@scope.run_action('delete')
				true
			return true
		$.post(
			"/task/actions/", 
			data,
			(r) =>
				@get_tasks()
				alertify.success("Action effectuée avec succès!")
				true
		)
		true

	get_tasks_selected: () =>

		return $.grep(@scope.tasks, (item, n) ->
			return item.checked?
		)

	get_tasks: =>
		
		@scope.tasks = @Task.query()
		@scope.tasks.$promise.then (result) =>
			@scope.tasks = result.results
			true

app.controller 'BacklogController', BacklogController