class ModalTaskController

	@$inject: ['$scope', '$rootScope', 'Task', 'Employee', 'Sprint', '$http', '$q' ] 

	constructor: (@scope, $rootScope, Task, Employee, Sprint, $http, $q) ->

		@Task                    = Task
		@Employee                = Employee
		@Sprint                  = Sprint

		@http                    = $http
		@rootScope               = $rootScope
		@q                       = $q

		@scope.task        = {}
		@scope.new_task    = @new_task
		@scope.update_task = @update_task
		@scope.record_task = @record_task
		@scope.delete_task = @delete_task
		$('#modal_task_edit .datetimepicker2').datetimepicker({
			autoclose: true,
		})
		@scope.$on('modal_task', (event, task) =>
			if task.id?
				@update_task(task)
			else
				@new_task()
			true
		)
		true


	load_employees : () =>

		deferred = @q.defer()
		@Employee.query().$promise.then (r) =>
			deferred.resolve(r.results)
		return deferred.promise


	load_sprints : () =>

		deferred = @q.defer()
		@Sprint.query().$promise.then (r) =>
			deferred.resolve(r.results)
		return deferred.promise


	load_data: () =>

		deferred = @q.defer()
		@Sprint.query().$promise.then (r) =>
			deferred.resolve(r.results)
		return deferred.promise		


	init: () =>

		@scope.task            = {}
		true

	new_task: () =>

		@init()
		@q.all([

			@load_employees(),
			@load_sprints()

		]).then (response) =>

			@scope.employees = response[0]
			@scope.sprints   = response[1]
			@scope.sprints.unshift { 'name': 'Selectionnez un sprint' }
			$('#modal_task_edit').modal 'show'
			true
		true

	update_task: (task) =>

		@init()
		@q.all([
			@Task.get({id: task.id}).$promise,
			@load_employees(),
			@load_sprints()
		]).then (response) =>
			task             = response[0]
			@scope.employees = response[1]
			@scope.sprints   = response[2]
			@scope.sprints.unshift { 'name': 'Selectionnez un sprint' }
			@scope.task            = task
			@scope.task.status     = task.status.toString()
			@scope.task.date_start = get_utc_datetime(task.date_start)
			@scope.task.date_end   = get_utc_datetime(task.date_end)
			# task, (e.id.toString() for e in task.employees) Select pre_loaded
			$('#modal_task_edit').modal 'show'
			true
		true

	record_task : () =>

		task            = angular.copy @scope.task
		task.date_start = set_utc_datetime(task.date_start)
		task.date_end   = set_utc_datetime(task.date_end)
		# task.sprint     = task.sprint.id
		if task.date_start == ""
			delete task.date_start
		if task.date_end == ""
			delete task.date_end
		if not task.id
			@Task.save( task ).$promise.then( 
				(r) =>
					@rootScope.$broadcast("task_recorded", r)
					@init()
					alertify.success("Tâche enregistrée avec succès!")
				, 
				(r) =>
					alertify.error("Erreur lors de l'enregistrement de la tâche")
					@scope.task.errors = r.data
			)
		else
			@Task.update( task ).$promise.then( 
				(r) =>
					@rootScope.$broadcast("task_recorded", r)
					alertify.success("Tâche modifiée avec succès!")
					$('#modal_sprint').modal 'hide'
				, 
				(r) =>
					alertify.error("Erreur lors de l'enregistrement de la tâche")
					@scope.task.errors = r.data
			)
		true

	delete_task : (task) =>

		alertify.confirm(
			"Supprimer cette tâche?", 
			() => 
				@Task.delete(task).$promise.then (r) =>
					alertify.success("Tâche supprimée avec succès")
					@get_tasks()
					true
		)
		true


app.controller 'ModalTaskController', ModalTaskController