<template>
  <v-container>
    <v-layout
      text-xs-center
      wrap
    >
      <v-flex>
        <!-- IMPORTANT PART! -->

<h1><p> Fifa Career Mode Optimizer </p></h1>
<p> Stressed about a new career challenge ahead? Limited financial capabilities in your "Road To Glory" adventure? <b>We're here to help.</b></p>

<img src="@/assets/transfer.jpeg">

<p> <b>Careers Optimizer</b> uses linear and integer programming to optimize your team build up for your next Fifa Careers Adventure.</p>
<p> You can choose from two options: </p>

<ul>
  <li>Optimize Overall: Set your current financial capabilities, choose your optimal formation and a maximum age per player. This tool will try to find the best overall team.</li>
  <li>Optimize Potential: Similar to the previous one, but with the added component of setting a maximum <b>current</b> overall. This model will optimize the future potential of players. </li>
  <p></p>
</ul>

<p> You can choose an infinite number of players, starting from 1. The team formation visualization will only show up when you choose 11 (with a normal formation).</p>
<p> <b>Optimize below! </b> </p>

<form>
          <v-text-field
            v-model="budget"
            label="Budget"
            required
          ></v-text-field>

          <v-text-field
            v-model="budget_wage"
            label="Budget Wage"
            required
          ></v-text-field>

          <v-text-field
            v-model="gk"
            label="Goalkeeper"
            required
          ></v-text-field>

           <v-text-field
            v-model="defs"
            label="Defenders"
            required
          ></v-text-field>

           <v-text-field
            v-model="mid"
            label="Midfielders"
            required
          ></v-text-field>

           <v-text-field
            v-model="att"
            label="Attackers"
            required
          ></v-text-field>

           <v-text-field
            v-model="max_age"
            label="Maximum Age"
            required
          ></v-text-field>

           <v-text-field
            v-model="max_overall"
            label="Maximum Overall (Potential Only)"
            required
          ></v-text-field>


<v-btn @click="submit('http://localhost:5000/overall')">Optimize Overall</v-btn>
<v-btn @click="submit('http://localhost:5000/potential')">Optimize Potential</v-btn>
          <v-btn @click="clear">clear</v-btn>
        </form>
<br/>
        <br/>
<h1 v-if="solution"><p> Solution: <span v-html=" solution">{{solution}}</span></p></h1>
<!--h1> <img v-bind:src="'data:image/jpg;base64,'+  radar" /> </h1-->
<!-- END: IMPORTANT PART! -->
  <div v-if="images">

    <div class="col-md-12" v-for="(image, index) in images" :key="index">
      <!--h1>{{index}}</h1-->
        <img v-bind:src = "'data:image/jpg;base64,' + image.image" class="img-fluid" style="margin-left: -800px;" :key="index" />
    </div>
  </div>


  <div v-if="formation">
    <img v-bind:src = "'data:image/jpg;base64,' + formation.formation" class="img-fluid" style="margin-left: -100px;" />
  </div>

  <h1 v-if="loading"><p> Loading... </p></h1>

      
      </v-flex>
    </v-layout>
  </v-container>
</template>
<script>
  import axios from 'axios'
  //import qs from 'qs'


export default {
    name: 'HelloWorld',
    data: () => ({
      budget: '',
      budget_wage: '',
      players: '',
      gk: '',
      defs: '',
      mid: '',
      att: '',
      max_age: '',
      overall_team: null,
      solution:null,
      max_overall:'',
      images: [],
      formation: null,
      loading: false
    }),
    methods: {
    submit(url) {
      this.solution = false;
      this.images = false;
      this.formation = false;
      this.loading = true;
      axios.post(url, {
        budget: this.budget,
        budget_wage: this.budget_wage,
        players: this.players,
        gk: this.gk,
        defs: this.defs,
        mid: this.mid,
        att: this.att,
        max_age: this.max_age,
        max_overall: this.max_overall
      })
      .then((response) => {
        this.loading = false;
        console.log(response);
        this.overall_team = response.data.overall;
        this.solution = response.data.solution.replace(/(\\r)*\\n/g, '<br>');

        const requests = [];

        this.loading = true;
        this.overall_team.forEach((playerid) => {
          console.log(playerid)
          
          requests.push(axios.post('http://localhost:5000/stats', {
            playerid
          }));
        });

        axios.all(requests).then(axios.spread((...responses) => {
            this.images = responses.map(obj => obj.data);
            this.loading=false;
        }));

        const team = JSON.stringify(this.overall_team).replaceAll('"', '').split('[')[1].split(']')[0].trim().split(' ').join(',').trim();
        this.loading=true;
        axios.post('http://localhost:5000/formation', {
          team: team,
          defs: this.defs,
          mid: this.mid,
          att: this.att
        }).then(response => {
          this.loading=false;
          this.formation = response.data;
        });
      })
    },
    clear () {
       this.budget = '',
       this.budget_wage = '',
       this.players = '',
       this.gk = '',
       this.defs = '',
       this.mid = '',
       this.att = '',
       this.max_age = '',
       this.max_overall = ''
    }
  }
}
</script>
