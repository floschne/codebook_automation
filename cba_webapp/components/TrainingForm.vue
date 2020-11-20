<template>
  <div>
    <b-form v-if="show" @submit="onSubmit">
      <!--      CODEBOOK-->
      <b-form-group>
        <b-form-group
          id="label-name"
          label="Name"
          label-for="input-name"
          description="Name of the model/Codebook"
          label-cols-md="4"
          label-cols-lg="2"
        >
          <b-form-input
            id="input-name"
            v-model="form.cb.name"
            placeholder="Enter model/Codebook name"
            aria-describedby="input-model-name-feedback"
            required
            trim
            :state="nameState"
          />

          <b-form-invalid-feedback id="input-model-name-feedback">
            Enter at least one character and no whitespaces allowed!
          </b-form-invalid-feedback>
        </b-form-group>

        <b-form-group
          id="label-tags"
          label="Tags/Labels"
          label-for="input-tags"
          label-cols-md="4"
          label-cols-lg="2"
          description="Labels of the model / Tags of the Codebook"
        >
          <b-form-tags
            id="input-tags"
            v-model="form.cb.tags"
            input-id="input-tags"
            separator=" ,;"
            placeholder="Enter Tags/Labels separated by comma, semicolon or space"
            aria-describedby="input-tags-feedback"
            :state="tagsState"
            remove-on-delete
            required
          />

          <b-form-invalid-feedback id="input-tags-feedback">
            Enter at least two tags!
          </b-form-invalid-feedback>
        </b-form-group>
      </b-form-group>
      <!--              DATASET VERSION -->
      <b-form-group
        id="label-dataset-version"
        label="Dataset Version"
        label-for="input-dataset-version"
        description="Version of the dataset that will be used for training and testing."
        label-cols-md="4"
        label-cols-lg="2"
      >
        <b-form-input
          id="input-dataset-version"
          v-model="form.dataset_version"
          type="text"
          placeholder="default"
          aria-describedby="input-dataset-version-feedback"
          trim
          :state="datasetVersionState"
        />

        <b-form-invalid-feedback id="input-dataset-version-feedback">
          No whitespaces allowed!
        </b-form-invalid-feedback>
      </b-form-group>

      <!--            MODEL VERSION   -->
      <b-form-group
        id="label-model-version"
        label="Model Version"
        label-for="input-model-version"
        description="Version of the model that will be created."
        label-cols-md="4"
        label-cols-lg="2"
      >
        <b-form-input
          id="input-model-version"
          v-model="form.model_version"
          type="text"
          placeholder="default"
          aria-describedby="input-model-version-feedback"
          trim
          :state="modelVersionState"
        />

        <b-form-invalid-feedback id="input-model-version-feedback">
          No whitespaces allowed!
        </b-form-invalid-feedback>
      </b-form-group>

      <b-button v-b-toggle.collapse-model-config variant="secondary" size="sm" class="w-100 mt-1 mb-1">
        Toggle Model Config (or use default)
      </b-button>
      <b-collapse id="collapse-model-config" class="mt-2 mb-2">
        <!--      MODEL CONFIG-->
        <b-form-group>
          <!--      Embedding    -->
          <b-form-group
            id="label-embedding-type"
            label="Embedding Type"
            label-for="input-embedding-type"
            description="Tensorflow Hub URL to an embedding type."
            label-cols-md="4"
            label-cols-lg="2"
          >
            <b-form-input
              id="input-embedding-type"
              v-model="form.model_config.embedding_type"
              placeholder="Checkout Tensorflow HUB for embedding types."
              aria-describedby="input-embedding-type-feedback"
              type="url"
              required
              trim
            />

            <b-form-invalid-feedback id="input-model-name-feedback">
              Enter valid URL!
            </b-form-invalid-feedback>
          </b-form-group>

          <!--      Hidden Units    -->
          <b-form-group
            id="label-hidden-units"
            label="Layers / Hidden Units"
            label-for="input-hidden-units"
            label-cols-md="4"
            label-cols-lg="2"
            description="Stack of layers with their hidden units"
          >
            <HiddenUnitsInput @added-layer="updateHiddenUnits" />
          </b-form-group>

          <!--      Dropout    -->
          <b-form-group
            id="label-dropout-type"
            label="Dropout"
            label-for="input-dropout-type"
            description="Dropout fraction"
            label-cols-md="4"
            label-cols-lg="2"
          >
            <b-input-group>
              <b-input-group-prepend>
                <b-badge variant="primary" style="min-width: 2.5rem">
                  <span>{{ form.model_config.dropout }}</span>
                </b-badge>
              </b-input-group-prepend>

              <b-form-input
                id="input-dropout-type"
                v-model="form.model_config.dropout"
                aria-describedby="input-embedding-type-feedback"
                type="range"
                min="0"
                max="1"
                step="0.01"
                required
                trim
              />
            </b-input-group>
          </b-form-group>

          <!--      Optimizer    -->
          <b-form-group
            id="label-optimizer-type"
            label="Optimizer"
            label-for="input-optimizer-type"
            label-cols-md="4"
            label-cols-lg="2"
          >
            <b-form-select id="input-optimizer-type" v-model="form.model_config.optimizer" :options="optimizers" required />
          </b-form-group>

          <!--      Activation Function    -->
          <b-form-group
            id="label-act-fn-type"
            label="Activation Function"
            label-for="input-act-fn-type"
            label-cols-md="4"
            label-cols-lg="2"
          >
            <b-form-select id="input-act-fn-type" v-model="form.model_config.activation_fn" :options="activationFunctions" required />
          </b-form-group>

          <!--      Early Stopping    -->
          <b-form-group
            id="label-early-stopping"
            label="Early Stopping"
            label-for="input-optimizer-type"
            label-cols-md="4"
            label-cols-lg="2"
          >
            <b-form-checkbox
              id="input-early-stopping"
              v-model="form.model_config.early_stopping"
              value="true"
              unchecked-value="false"
            >
              {{ form.model_config.early_stopping }}
            </b-form-checkbox>
          </b-form-group>
        </b-form-group>
      </b-collapse>

      <b-button v-b-toggle.collapse-training-config variant="secondary" size="sm" class="w-100 mt-1 mb-1">
        Toggle Training Config (or use default)
      </b-button>
      <b-collapse id="collapse-training-config" class="mt-2">
        <!--      TRAINING BATCH SIZE -->
        <b-form-group
          id="label-batch-size-train"
          label="Training Batch Size"
          label-for="input-batch-size-train"
          label-cols-md="4"
          label-cols-lg="2"
        >
          <b-form-input
            id="input-batch-size-train"
            v-model="form.batch_size_train"
            type="number"
            placeholder="Enter training batch size"
            trim
            :state="bsTrainState"
          />
        </b-form-group>

        <!--      TEST BATCH SIZE -->
        <b-form-group
          id="label-batch-size-test"
          label="Test Batch Size"
          label-for="input-batch-size-test"
          label-cols-md="4"
          label-cols-lg="2"
        >
          <b-form-input
            id="input-batch-size-test"
            v-model="form.batch_size_test"
            type="number"
            placeholder="Enter test batch size"
            trim
            :state="bsTestState"
          />
        </b-form-group>

        <!--      MAX STEPS TRAIN -->
        <b-form-group
          id="label-max-steps-train"
          label="Maximum steps during training"
          label-for="input-max-steps-train"
          label-cols-md="4"
          label-cols-lg="2"
        >
          <b-form-input
            id="input-max-steps-train"
            v-model="form.max_steps_train"
            type="number"
            placeholder="Enter maximum steps during training"
            trim
            :state="maxStepsTrainState"
          />
        </b-form-group>

        <!--      MAX STEPS TEST -->
        <b-form-group
          id="label-max-steps-test"
          label="Maximum steps during testing"
          label-for="input-max-steps-test"
          label-cols-md="4"
          label-cols-lg="2"
        >
          <b-form-input
            id="input-max-steps-test"
            v-model="form.max_steps_test"
            type="number"
            placeholder="Enter maximum steps during testing"
            trim
            :state="maxStepsTestState"
          />
        </b-form-group>
      </b-collapse>

      <b-button
        class="w-100"
        type="submit"
        variant="primary"
        :disabled="!(totalFormState)"
      >
        Start Training!
      </b-button>
    </b-form>
  </div>
</template>

<script>
import HiddenUnitsInput from '@/components/HiddenUnitsInput'
export default {
  name: 'TrainingForm',
  components: { HiddenUnitsInput },
  emits: ['training-form-submit'],
  data () {
    return {
      optimizers: ['Adam', 'SGD', 'Adagrad', 'RMSProp', 'Ftrl'],
      activationFunctions: ['relu', 'sigmoid', 'tanh', 'exponential'],
      show: true,
      form: {
        cb: {
          name: '',
          tags: []
        },
        model_config: {
          embedding_type: 'https://tfhub.dev/google/universal-sentence-encoder/2',
          hidden_units: [1024, 1024, 512, 64],
          dropout: 0.2,
          optimizer: 'Adam',
          early_stopping: false,
          activation_fn: 'relu'
        },
        model_version: 'default',
        dataset_version: 'default',
        batch_size_train: 32,
        batch_size_test: 32,
        max_steps_train: 100,
        max_steps_test: 100
      }
    }
  },
  computed: {
    modelVersionState () {
      return this.form.model_version.search('\\s') < 0
    },
    datasetVersionState () {
      return this.form.dataset_version.search('\\s') < 0
    },
    nameState () {
      return this.form.cb.name.search('\\s') < 0 && this.form.cb.name.length >= 1
    },
    tagsState () {
      return this.form.cb.tags.length >= 2
    },
    hiddenUnitesState () {
      return this.form.model_config.hidden_units.length >= 1
    },
    bsTrainState () {
      return this.form.batch_size_train >= 1
    },
    bsTestState () {
      return this.form.batch_size_test >= 1
    },
    maxStepsTrainState () {
      return this.form.max_steps_train >= 1
    },
    maxStepsTestState () {
      return this.form.max_steps_test >= 1
    },
    totalFormState () {
      return this.modelVersionState &&
        this.datasetVersionState &&
        this.nameState &&
        this.tagsState &&
        this.hiddenUnitesState &&
        this.bsTrainState &&
        this.bsTestState &&
        this.maxStepsTrainState &&
        this.maxStepsTestState
    }
  },
  methods: {
    onSubmit (evt) {
      evt.preventDefault()
      this.$emit('training-form-submit', this.form)
      console.log('auasdbuabsdassubbbbbbbbbbbbbbbbbb')
    },
    updateHiddenUnits (hidden) {
      this.hidden_units = hidden
    }
  }
}
</script>

<style scoped>

</style>
