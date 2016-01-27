let TaskPage = React.createClass({
  loadTasksFromServer: function(append) {
    let tasks = this.state.data;
    if (!append) {
      tasks = [];
      let filters = this.state.filters;
      filters.page = 1;
      this.setState({filters: filters});
    }
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      data: this.state.filters,
      traditional: true,
      success: function(data) {
        this.setState({
          data: tasks.concat(data.results),
          moreTasks: data.next != null
        });
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  loadTeamsFromServer: function() {
    $.ajax({
      url: this.props.team_url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({teams: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.team_url, status, err.toString());
      }.bind(this)
    });
  },
  loadProjectsFromServer: function() {
    $.ajax({
      url: this.props.project_url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({projects: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.project_url, status, err.toString());
      }.bind(this)
    });
  },
  loadTypesFromServer: function() {
    $.ajax({
      url: this.props.type_url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({types: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.type_url, status, err.toString());
      }.bind(this)
    });
  },
  loadMoreTasks: function() {
    let filters = this.state.filters;
    filters.page ++;
    this.setState({filters: filters});
    this.loadTasksFromServer(true);
  },
  getInitialState: function() {
    return {
      data: [],
      filters: {search: '', execution_time: [], team: [], project: [], type: [], page: 1},
      moreTasks: false,
      teams: [],
      projects: [],
      types: []
    };
  },
  componentDidMount: function() {
    this.loadTasksFromServer();
    this.loadTeamsFromServer();
    this.loadProjectsFromServer();
    this.loadTypesFromServer();
  },
  render: function() {
    return (
      <div className="taskPage">
        <TaskFilters filters={this.state.filters}
                     onFilterChange={this.loadTasksFromServer}
                     teams={this.state.teams}
                     types={this.state.types}
                     projects={this.state.projects}/>
        <TaskList data={this.state.data} onLoadMore={this.loadMoreTasks} moreTasks={this.state.moreTasks} />
      </div>
    );
  }
});

let TaskFilters = React.createClass({
  handleSearchChange: function(e) {
    this.props.filters.search = e.target.value;
    this.props.onFilterChange();
  },
  render: function() {
    return (
      <div className="task-filters">
        <form method="get" className="filters">
          <fieldset>
            <SearchFilter {...this.props} />
            <ETFilter {...this.props} />
            <TeamFilter {...this.props} />
            <ProjectFilter {...this.props} />
            <TypeFilter {...this.props} />
          </fieldset>
        </form>
      </div>
    );
  }
});

let SearchFilter = React.createClass({
  handleChange: function(e) {
    this.props.filters.search = e.target.value;
    this.props.onFilterChange();
  },
  render: function() {
    return (
      <p>
        <input type="text" id="search" placeholder="Search for tasks" onChange={this.handleChange} />
      </p>
    );
  }
});

let ETFilter = React.createClass({
  render: function() {
    let etNodes = [15, 30, 45, 60].map(function(executionTime) {
      return (
        <ET executionTime={executionTime}
            key={executionTime}
            {...this.props} />
      );
    }, this);
    return (
      <div className="et-filter">
        <p>Estimated minutes to complete:</p>
        <p>
          {etNodes}
        </p>
      </div>
    );
  }
});

let ET = React.createClass({
  handleChange: function(e) {
    let executionTime = this.props.filters.execution_time;
    if (e.target.checked) {
      executionTime.push(e.target.value);
    } else {
      executionTime.splice($.inArray(e.target.value, executionTime), 1);
    }
    this.props.onFilterChange();
  },
  render: function() {
    let etId = 'et' + this.props.executionTime;
    return (
      <label htmlFor={etId}>
        <input id={etId} value={this.props.executionTime} type="checkbox" onClick={this.handleChange} />
        {this.props.executionTime}
      </label>
    );
  }
});

let TeamFilter = React.createClass({
  getInitialState: function() {
    return {
      expanded: false
    }
  },
  handleToggle: function(e) {
    this.setState({expanded: !this.state.expanded});
  },
  render: function () {
    let teamNodes = this.props.teams.map(function(team) {
      if (this.state.expanded || $.inArray(team.id.toString(), this.props.filters.team) > -1) {
        return (
          <Team id={team.id}
                name={team.name}
                url={team.url}
                key={team.id}
                {...this.props} />
        );
      }
    }, this);
    return (
      <div>
        <span className="filter-heading">Teams</span>
        <span className="filter-toggle" onClick={this.handleToggle}> {(this.state.expanded) ? '-':'+'} </span>
        <ul>
          {teamNodes}
        </ul>
      </div>
    );
  }
});

let Team = React.createClass({
  handleChange: function(e) {
    let team = this.props.filters.team;
    if (e.target.checked) {
      team.push(e.target.value);
    } else {
      team.splice($.inArray(e.target.value, team), 1);
    }
    this.props.onFilterChange();
  },
  render: function() {
    let teamId = 'team' + this.props.id;
    return (
      <li>
        <label htmlFor={teamId}>
          <input id={teamId} value={this.props.id} type="checkbox" onClick={this.handleChange} />
          {this.props.name}
        </label>
      </li>
    );
  }
});

let ProjectFilter = React.createClass({
  getInitialState: function() {
    return {
      expanded: false
    }
  },
  handleToggle: function(e) {
    this.setState({expanded: !this.state.expanded});
  },
  render: function () {
    let projectNodes = this.props.projects.map(function(project) {
      if (this.state.expanded || $.inArray(project.id.toString(), this.props.filters.project) > -1) {
        return (
          <Project id={project.id}
                   name={project.name}
                   key={project.id}
            {...this.props} />
        );
      }
    }, this);
    return (
      <div>
        <span className="filter-heading">Projects</span>
        <span className="filter-toggle" onClick={this.handleToggle}> {(this.state.expanded) ? '-':'+'} </span>
        <ul>
          {projectNodes}
        </ul>
      </div>
    );
  }
});

let Project = React.createClass({
  handleChange: function(e) {
    let project = this.props.filters.project;
    if (e.target.checked) {
      project.push(e.target.value);
    } else {
      project.splice($.inArray(e.target.value, project), 1);
    }
    this.props.onFilterChange();
  },
  render: function() {
    let projectId = 'project' + this.props.id;
    return (
      <li>
        <label htmlFor={projectId}>
          <input id={projectId} value={this.props.id} type="checkbox" onClick={this.handleChange} />
          {this.props.name}
        </label>
      </li>
    );
  }
});

let TypeFilter = React.createClass({
  getInitialState: function() {
    return {
      expanded: false
    }
  },
  handleToggle: function(e) {
    this.setState({expanded: !this.state.expanded});
  },
  render: function () {
    let typeNodes = this.props.types.map(function(type) {
      if (this.state.expanded || $.inArray(type.id.toString(), this.props.filters.type) > -1) {
        return (
          <Type id={type.id}
                name={type.name}
                key={type.id}
            {...this.props} />
        );
      }
    }, this);
    return (
      <div>
        <span className="filter-heading">Types</span>
        <span className="filter-toggle" onClick={this.handleToggle}> {(this.state.expanded) ? '-':'+'} </span>
        <ul>
          {typeNodes}
        </ul>
      </div>
    );
  }
});

let Type = React.createClass({
  handleChange: function(e) {
    let type = this.props.filters.type;
    if (e.target.checked) {
      type.push(e.target.value);
    } else {
      type.splice($.inArray(e.target.value, type), 1);
    }
    this.props.onFilterChange();
  },
  render: function() {
    let typeId = 'type' + this.props.id;
    return (
      <li>
        <label htmlFor={typeId}>
          <input id={typeId} value={this.props.id} type="checkbox" onClick={this.handleChange} />
          {this.props.name}
        </label>
      </li>
    );
  }
});

let TaskList = React.createClass({
  render: function() {
    let taskNodes = this.props.data.map(function(task) {
      return (
        <Task name={task.name}
              short_description={task.short_description}
              url={task.url}
              edit_url={task.edit_url}
              key={task.id}>
          {task.short_description}
        </Task>
      );
    });
    let loadMore;
    if (this.props.moreTasks) {
      loadMore = <LoadMoreButton onLoadMore={this.props.onLoadMore} />
    }
    return (
      <div className="task-list-container">
        <ol className="task-list">
          {taskNodes}
        </ol>
        {loadMore}
      </div>
    );
  }
});

let LoadMoreButton = React.createClass({
  render: function() {
    return (
      <a className="button" onClick={this.props.onLoadMore}>Load more</a>
    );
  }
})

let Task = React.createClass({
  render: function() {
    console.log('rendering task');
    let editLink;
    if (this.props.edit_url) {
      editLink = <EditLink edit_url={this.props.edit_url} />
    }
    return (
      <li>
        <p>
          <a className="task-name" href={this.props.url}>{this.props.name}</a>
          {editLink}
        </p>
        <p className="task-desc">{this.props.children.toString()}</p>
      </li>
    );
  }
});

let EditLink = React.createClass({
  render: function() {
    return (
      <span> | <a className="edit-task" href={this.props.edit_url}>Edit</a></span>
    );
  }
})


ReactDOM.render(
    <TaskPage url="/api/v1/task"
              team_url="/api/v1/taskteam"
              project_url="/api/v1/taskproject"
              type_url="/api/v1/tasktype" />,
    document.getElementById('content')
);
