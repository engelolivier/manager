class SprintController

	@$inject: ['$scope', '$rootScope', 'Task', 'Sprint', '$http', '$q' ] 

	constructor: (@scope, $rootScope, Task, Sprint, $http, $q) ->

		@Sprint                    = Sprint
		@Task                      = Task
		@scope.tasks               = []
		@scope.sprints             = []
		@scope.modal_new_sprint    = @modal_new_sprint
		@scope.record_sprint       = @record_sprint
		@scope.modal_update_sprint = @modal_update_sprint
		@scope.delete_sprint       = @delete_sprint
		@scope.modal_task          = @modal_task
		@scope.task_dropped        = @task_dropped
		@q                         = $q
		@rootScope                 = $rootScope
		$('#modal_sprint .datetimepicker2').datetimepicker({
			minView: 'month',
			format : 'dd/mm/yyyy',
			autoclose: true,
		})
		@init_tasks()
		@scope.$on("task_recorded", (event, task) =>
			@load_tasks().then () =>
				t = @get_list_task( task )
				if t 
					t.label = task.name
				true
			true
		)
		@load_tasks()
		true

	init_tasks : () =>

		@scope.models = {
			selected: null,
			lists: [ [], [], [] ]
		}
		true

	load_tasks : () =>

		deferred = @q.defer()
		@init_tasks()
		@get_sprints().then (r) =>
			if r.results.length
				last_sprint = r.results[0]
				@get_tasks(last_sprint.id).then (tasks) =>
					for task in tasks
						@scope.models.lists[task.status].push id : task.id, label: task.name
			deferred.resolve(r)
			true
		return deferred.promise


	task_dropped: (event, index, task, $index) =>

		new_task = { 'id' : task.id, 'status' : $index }
		#@Task.update({id : task.id}, new_task)
		$.post("task/change_status/" + task.id, new_task, () =>
			true
		)
		return task
		

	get_list_task : (init_task) =>

		for i, tasks of @scope.models.lists
			for j, task of tasks
				if task.id == init_task.id
					return task
		return null


	modal_task: (task) =>

		@rootScope.$broadcast('modal_task', task or {})
		true

	get_sprints: () ->

		deferred = @q.defer()
		@Sprint.query().$promise.then (r) =>
			@scope.sprints = r.results
			deferred.resolve(r)
		return deferred.promise

	get_tasks: (sprint) ->

		deferred = @q.defer()
		$.post("/sprint/tasks/" + sprint, (r) =>
			deferred.resolve(r)
		)
		return deferred.promise

	modal_init: () =>

		@scope.sprint_selected = {}
		true

	modal_new_sprint: () =>

		@modal_init()
		$('#modal_sprint').modal 'show'
		true


	modal_update_sprint : (sprint) =>

		@scope.sprint_selected            = angular.copy sprint
		@scope.sprint_selected.date_start = get_utc_date(@scope.sprint_selected.date_start)
		@scope.sprint_selected.date_end   = get_utc_date(@scope.sprint_selected.date_end)
		$('#modal_sprint').modal 'show'
		true

	record_sprint: () =>

		sprint_selected            = angular.copy @scope.sprint_selected
		sprint_selected.date_start = set_utc_date(@scope.sprint_selected.date_start)
		sprint_selected.date_end   = set_utc_date(@scope.sprint_selected.date_end)
		if sprint_selected.id
			@Sprint.update( sprint_selected ).$promise.then (r) =>
				@get_sprints()
				$('#modal_sprint').modal 'hide'
				true
		else
			@Sprint.save( sprint_selected ).$promise.then (r) =>
				@get_sprints()
				@modal_init()
				true
		true

	delete_sprint: (sprint) =>

		alertify.confirm("Êtes-vous sûr de voiloire supprimer ce sprint?", () => 
			@Sprint.delete({id: sprint.id}).$promise.then (r) =>
				@get_sprints()
				true
		)
		true

app.controller 'SprintController', SprintController