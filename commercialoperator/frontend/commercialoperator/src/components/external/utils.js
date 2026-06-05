import api from './api';
import { helpers } from '@/utils/hooks';

export default {
    fetchProfile: function () {
        return new Promise((resolve, reject) => {
            helpers.fetchUrl(api.profile).then(
                (response) => {
                    resolve(response);
                },
                (error) => {
                    reject(error);
                }
            );
        });
    },
    fetchProposal: function (id) {
        return new Promise((resolve, reject) => {
            helpers.fetchUrl(helpers.add_endpoint_json(api.proposals, id)).then(
                (response) => {
                    resolve(response);
                },
                (error) => {
                    reject(error);
                }
            );
        });
    },
    fetchCountries: function () {
        return new Promise((resolve, reject) => {
            helpers.fetchUrl(api.countries).then(
                (response) => {
                    resolve(response);
                },
                (error) => {
                    reject(error);
                }
            );
        });
    },
    fetchOrganisation: function (id) {
        return new Promise((resolve, reject) => {
            helpers
                .fetchUrl(helpers.add_endpoint_json(api.organisations, id))
                .then(
                    (response) => {
                        resolve(response);
                    },
                    (error) => {
                        reject(error);
                    }
                );
        });
    },
};
