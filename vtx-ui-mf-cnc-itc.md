# 📦 Collected Source Files

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress-component-base.ts`

```ts
import * as webpackPreprocessor from '@cypress/webpack-preprocessor';
import { getWebpackPreprocessorOptions } from '@vertexinc/vtx-react-scripts';
import { defineConfig } from 'cypress';

// eslint-disable-next-line import/no-default-export
export default defineConfig({
  // These settings apply everywhere unless overridden
  chromeWebSecurity: false,
  fixturesFolder: 'cypress/fixtures',
  numTestsKeptInMemory: 2,
  projectId: '5r3vqt',
  e2e: {
    specPattern: 'cypress/integration/**/*.spec.ts',
    supportFile: 'cypress/support/index.ts',
    setupNodeEvents(on, config) {
      // The following line allows for necessary values (eg. GitHub secrets like AUTH0_IDP_PASSWORD_DEVELOPMENT)
      // to be made available as Cypress environment variables.
      config.env = { ...config.env, ...process.env };

      const webpackPreprocessorOptions = getWebpackPreprocessorOptions();
      on('file:preprocessor', webpackPreprocessor(webpackPreprocessorOptions));

      return config;
    },
  },
});

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress-component-development.ts`

```ts
import { defineConfig } from 'cypress';
import { mergePartially } from 'merge-partially';
import baseConfig from './cypress-component-base';

export default {
  ...defineConfig(
    mergePartially.shallow(baseConfig, {
      env: {
        authSessionStorageKey: 'oidc.user:https://dev-auth.vtxdev.net:SgZmOOmYGqTdnXoE9i2w0t37PZr6VSEQ',
      },
      e2e: {
        baseUrl: 'https://dev-app.vtxdev.net/ui/transaction-tax-close',
      },
      component: {
        devServer: {
          framework: 'react',
          bundler: 'webpack',
        },
      },
    })
  ),
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/constants.ts`

```ts
export const constants = {
  BASE_HELP_URL: 'https://community.vertexinc.com/s/csh?topicname=CloudOSeriesHome.html&pubname=COSOverview',
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/browser-history.ts`

```ts
import { createBrowserHistory } from 'history';

export const history = createBrowserHistory();

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/datasource.ts`

```ts
import { api } from 'src/api/api';
import { RedirectResponse } from 'src/api/client';
import { resolve } from 'src/api/resolver';

const onError = (error: Error) => {
  window.console.error('Data Connections error', error);
  throw error;
};

export class RootDataSource {
  /**
   * Fetches User Permission information.
   * @static
   * @returns {UserPermissions}
   * @memberof RootDataSource
   */
  static async getUserPermissions(): Promise<unknown> {
    return resolve(
      api.fetchUserPermissions(),
      (res: Response | RedirectResponse) => (res as Response).json(),
      onError
    );
  }

  /**
   * Fetches Menu information.
   * @static
   * @returns {UMenuObject}
   * @memberof RootDataSource
   */
  static async getMenu(): Promise<unknown> {
    return resolve(api.fetchMenu(), (res: Response | RedirectResponse) => (res as Response).json(), onError);
  }
}

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/types.ts`

```ts
/** Profile and LoginUser interfaces are subsets of the oidc-client.Profile and oidc-client.User interfaces*/
export interface Profile {
  /** End-User's full name */
  name?: string;
  /** Given name(s) or first name(s) of the End-User */
  given_name?: string;
  /** Surname(s) or last name(s) of the End-User */
  family_name?: string;
  /** Shorthand name that the End-User wishes to be referred to at the RP, such as janedoe or j.doe. */
  preferred_username?: string;
  /** End-User's preferred e-mail address */
  email?: string;
}

export type UserRoleCode = 'acct-adm';

export interface Role {
  platformProductCode: string;
  userRoleCode: UserRoleCode /* (TODO J.Skjevling): Update this with enum when types are known */;
  userRoleName: string /* (TODO J.Skjevling): Update this with enum when types are known */;
}

export interface Tenant {
  id: string;
  name: string;
  type: string /* (TODO J.Skjevling): Update this with enum when types are known */;
  subType: string /* (TODO J.Skjevling): Update this with enum when types are known */;
  oraclePartyNumber: string;
}

export interface Feature {
  platformProductCode: string;
  featureCode: string;
  featureName: string /* (TODO J.Skjevling): Update this with enum when types are known */;
}

export interface Subscription {
  id: string;
  status: string /* (TODO J.Skjevling): Update this with enum when types are known */;
  features: Feature[];
}

export interface ErrorMessages {
  errorCode: string;
  errorMessage: string;
}

export type AlertType = 'error' | 'warning' | 'info' | 'success';

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/wrapped-process-env.ts`

```ts
const getOrThrowIfNotFound = (name: string): string => {
  const variable = process.env[name];
  if (variable == null) {
    throw new Error(`Environment variable ${name} not found`);
  }
  return variable.toString();
};

interface EnvironmentVariable {
  CONFIG_API_BASE_URL: string;
  LAUNCH_DARKLY_CLIENT_ID: string;
}

export const wrappedProcessEnv: EnvironmentVariable = {
  CONFIG_API_BASE_URL: getOrThrowIfNotFound('CONFIG_API_BASE_URL'),
  LAUNCH_DARKLY_CLIENT_ID: getOrThrowIfNotFound('LAUNCH_DARKLY_CLIENT_ID'),
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/utils/months-array.ts`

```ts
import { CONSTANTS } from '../shared/constants-en';

export const months = [
  CONSTANTS.MONTH_JAN,
  CONSTANTS.MONTH_FEB,
  CONSTANTS.MONTH_MAR,
  CONSTANTS.MONTH_APR,
  CONSTANTS.MONTH_MAY,
  CONSTANTS.MONTH_JUN,
  CONSTANTS.MONTH_JUL,
  CONSTANTS.MONTH_AUG,
  CONSTANTS.MONTH_SEP,
  CONSTANTS.MONTH_OCT,
  CONSTANTS.MONTH_NOV,
  CONSTANTS.MONTH_DEC,
];

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/utils/currency-formatting.ts`

```ts
// format number to US dollar
export const USDollar = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
});

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/pages/data-readiness/utils.ts`

```ts
import { TagColors } from '@vertexinc/vtx-ui-react-component-library';
import { DataReadinessStatus } from 'src/shared/constants-en';

export const dataReadinessStatusColor = (status: string) => {
  let statusColor: TagColors = 'default';
  switch (status) {
    case DataReadinessStatus.NOT_READY:
      statusColor = 'default';
      break;
    case DataReadinessStatus.NEEDS_REVIEW:
      statusColor = 'red';
      break;
    case DataReadinessStatus.VALIDATED_DATA:
      statusColor = 'green';
      break;

    default:
      statusColor = 'default';
  }

  return statusColor;
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/pages/data-readiness/types.ts`

```ts
import { EntityApiData, TableEntity } from 'src/components/entity-table/types';
import { FilingPeriodApiData, FilingPeriodSelectOption } from 'src/components/filing-period-select/types';
import { DataReadinessStatus, EntityCompletenessCategory } from 'src/shared/constants-en';

export type EntityCompletenessDetailsValue = {
  completenessCategory: EntityCompletenessCategory;
  currentPeriodTotal: number;
  differencePercentage: number;
  previousPeriodTotal: number;
};
export interface EntityCompletenessDetails {
  [key: string]: EntityCompletenessDetailsValue[];
}

export interface EntityCompletenessApiData {
  currentPeriodNumber: number;
  currentPeriodEndDate: string;
  currentPeriodStartDate: string;
  entityDataCompletenessDetails: EntityCompletenessDetails;
  previousPeriodNumber: number;
  previousPeriodEndDate: string;
  previousPeriodStartDate: string;
}

export interface EntityCompletenessTable {
  completenessCategory: EntityCompletenessCategory.BASIS;
  previousPeriodTotal: number;
  currentPeriodTotal: number;
  differencePercentage: number;
}

export const sampleCompletenessApiData = {
  currentPeriodNumber: 3,
  currentPeriodStartDate: '2025-03-01T14:10:02.758Z',
  currentPeriodEndDate: '2025-03-31T14:10:02.758Z',
  previousPeriodNumber: 2,
  previousPeriodStartDate: '2025-02-01T14:10:02.758Z',
  previousPeriodEndDate: '2025-02-28T14:10:02.758Z',
  entityDataCompletenessDetails: {
    Basis: {
      completenessCategory: EntityCompletenessCategory.BASIS,
      previousPeriodTotal: 4000342.0,
      currentPeriodTotal: 3000342.0,
      differencePercentage: 22.5,
    },
    Tax: {
      completenessCategory: EntityCompletenessCategory.TAX,
      previousPeriodTotal: 260000.0,
      currentPeriodTotal: 160000.0,
      differencePercentage: 33.3,
    },
  },
};

export interface DataReadinessTableContext {
  selectedPeriod: FilingPeriodSelectOption | null;
  entities: TableEntity[];
}

export interface EntityDetails {
  dataReadiness: string;
  endDate: string;
  entityId: string;
  entityName: string;
  missingFieldLines: number;
  notStandardizedLines: number;
  notValidatedLines: number;
  parentId: number;
  periodId: number;
  startDate: string;
  successfulLinesCount: number;
  successfulTransactionsCount: number;
  totalLinesCount: number;
  totalTransactionsCount: number;
}

export interface ColumnFilterItem {
  text: string;
  value: string | number | boolean;
  children?: ColumnFilterItem[];
}

export const sampleEntityDetailsApiData = {
  dataReadiness: 'string',
  endDate: '2025-03-19T14:10:02.758Z',
  entityId: 'string',
  entityName: 'string',
  missingFieldLines: 10,
  notStandardizedLines: 22,
  notValidatedLines: 300,
  parentId: 112233,
  periodId: 12345,
  startDate: '2025-03-19T14:10:02.758Z',
  successfulLines: 500,
  successfulTransactions: 6032,
  taxCloseStatus: 'string',
  totalLines: 7001,
  totalTransactions: 10098,
};

export const sampleFilingPeriodApiData: FilingPeriodApiData = {
  periods: [
    {
      fiscalYear: 2025,
      periodNumber: 7,
      periodId: '1',
      startDate: '2025-03-19T10:00:00.000Z',
      endDate: '2025-07-31T00:00:00.000Z',
    },
    {
      fiscalYear: 2024,
      periodNumber: 6,
      periodId: '2',
      startDate: '2024-06-01T00:00:00.000Z',
      endDate: '2024-06-30T00:00:00.000Z',
    },
    {
      fiscalYear: 2024,
      periodNumber: 5,
      periodId: '3',
      startDate: '2024-05-01T00:00:00.000Z',
      endDate: '2024-05-31T00:00:00.000Z',
    },
  ],
};
// TODO: remove later, Temporary data for the table
export const sampleEntityApiData: EntityApiData = {
  entityDataReadinessSummaries: [
    {
      entityId: '126c51536-a204-4dba-b6d6-68de782bde82',
      entityName: 'ABC Corporate',
      dataReadinessStatus: DataReadinessStatus.VALIDATED_DATA,
      parentEntityId: '',
      periodId: 202301,
      startDate: '2023-01-01',
      endDate: '2023-12-31',
      children: [
        {
          entityId: '4572e123-a8d8-40be-8938-74d65656671c',
          entityName: 'ABC Sales',
          dataReadinessStatus: DataReadinessStatus.NEEDS_REVIEW,
          parentEntityId: '126c51536-a204-4dba-b6d6-68de782bde82',
          periodId: 202301,
          startDate: '2023-01-01',
          endDate: '2023-12-31',
          children: [
            {
              entityId: '1234abcd-5678-efgh-ijkl-9012mnopqrst',
              entityName: 'ABC Sales East',
              dataReadinessStatus: DataReadinessStatus.NOT_READY,
              parentEntityId: '4572e123-a8d8-40be-8938-74d65656671c',
              periodId: 202301,
              startDate: '2023-01-01',
              endDate: '2023-12-31',
            },
            {
              entityId: '5678abcd-1234-efgh-ijkl-9012mnopqrst',
              entityName: 'ABC Sales West',
              dataReadinessStatus: DataReadinessStatus.VALIDATED_DATA,
              parentEntityId: '4572e123-a8d8-40be-8938-74d65656671c',
              periodId: 202301,
              startDate: '2023-01-01',
              endDate: '2023-12-31',
            },
          ],
        },
        {
          entityId: '4572e123-a8d8-40be-8938-74d656563122',
          entityName: 'XYZ Sales',
          dataReadinessStatus: DataReadinessStatus.NEEDS_REVIEW,
          parentEntityId: '126c51536-a204-4dba-b6d6-68de782bde82',
          periodId: 202301,
          startDate: '2023-01-01',
          endDate: '2023-12-31',
        },
      ],
    },
    {
      entityId: 'b1bd6b89-28bf-4696-bcbe-9c73a8d67a0d',
      entityName: 'DEF Corporate',
      dataReadinessStatus: DataReadinessStatus.NEEDS_REVIEW,
      parentEntityId: '',
      periodId: 202301,
      startDate: '2023-01-01',
      endDate: '2023-12-31',
      children: [
        {
          entityId: '749d0229-ca46-4d58-9454-6b72a4d71be3',
          entityName: '123 Sales',
          dataReadinessStatus: DataReadinessStatus.VALIDATED_DATA,
          parentEntityId: 'b1bd6b89-28bf-4696-bcbe-9c73a8d67a0d',
          periodId: 202301,
          startDate: '2023-01-01',
          endDate: '2023-12-31',
          children: [
            {
              entityId: '5678abcd-1234-efgh-ijkl-9012mnopqrst',
              entityName: '123 Sales West',
              dataReadinessStatus: DataReadinessStatus.NEEDS_REVIEW,
              parentEntityId: '749d0229-ca46-4d58-9454-6b72a4d71be3',
              periodId: 202301,
              startDate: '2023-01-01',
              endDate: '2023-12-31',
              children: [],
            },
            {
              entityId: '6789abcd-1234-efgh-ijkl-9012mnopqrst',
              entityName: '123 Sales East',
              dataReadinessStatus: DataReadinessStatus.NOT_READY,
              parentEntityId: '749d0229-ca46-4d58-9454-6b72a4d71be3',
              periodId: 202301,
              startDate: '2023-01-01',
              endDate: '2023-12-31',
              children: [],
            },
          ],
        },
      ],
    },
    {
      entityId: '3f70d4e6-42e0-4d93-9439-f11f917e233a',
      entityName: 'HIJ Corporate',
      dataReadinessStatus: DataReadinessStatus.NOT_READY,
      parentEntityId: '',
      periodId: 202301,
      startDate: '2023-01-01',
      endDate: '2023-12-31',
      children: [
        {
          entityId: '793a4837-f9ec-4726-bc57-691c7071777c',
          entityName: 'Z Sales',
          dataReadinessStatus: DataReadinessStatus.VALIDATED_DATA,
          parentEntityId: '3f70d4e6-42e0-4d93-9439-f11f917e233a',
          periodId: 202301,
          startDate: '2023-01-01',
          endDate: '2023-12-31',
          children: [
            {
              entityId: '9012abcd-3456-efgh-ijkl-7890mnopqrst',
              entityName: 'Z Sales North',
              dataReadinessStatus: DataReadinessStatus.NEEDS_REVIEW,
              parentEntityId: '793a4837-f9ec-4726-bc57-691c7071777c',
              periodId: 202301,
              startDate: '2023-01-01',
              endDate: '2023-12-31',
            },
            {
              entityId: '0123abcd-4567-efgh-ijkl-7890mnopqrst',
              entityName: 'Z Sales South',
              dataReadinessStatus: DataReadinessStatus.NOT_READY,
              parentEntityId: '793a4837-f9ec-4726-bc57-691c7071777c',
              periodId: 202301,
              startDate: '2023-01-01',
              endDate: '2023-12-31',
            },
          ],
        },
      ],
    },
    {
      entityId: 'af91e293-b030-4224-89bf-7f09a4a1d33f',
      entityName: 'KLM Corporate',
      dataReadinessStatus: DataReadinessStatus.NEEDS_REVIEW,
      parentEntityId: '',
      periodId: 202301,
      startDate: '2023-01-01',
      endDate: '2023-12-31',
      children: [
        {
          entityId: '95514b1b-5112-42f7-a729-f70444bd22f4',
          entityName: 'X Sales',
          dataReadinessStatus: DataReadinessStatus.VALIDATED_DATA,
          parentEntityId: 'af91e293-b030-4224-89bf-7f09a4a1d33f',
          periodId: 202301,
          startDate: '2023-01-01',
          endDate: '2023-12-31',
          children: [
            {
              entityId: '3456abcd-7890-efgh-ijkl-1234mnopqrst',
              entityName: 'X Sales South',
              dataReadinessStatus: DataReadinessStatus.NEEDS_REVIEW,
              parentEntityId: '95514b1b-5112-42f7-a729-f70444bd22f4',
              periodId: 202301,
              startDate: '2023-01-01',
              endDate: '2023-12-31',
            },
            {
              entityId: '4567abcd-7890-efgh-ijkl-1234mnopqrst',
              entityName: 'X Sales North',
              dataReadinessStatus: DataReadinessStatus.NOT_READY,
              parentEntityId: '95514b1b-5112-42f7-a729-f70444bd22f4',
              periodId: 202301,
              startDate: '2023-01-01',
              endDate: '2023-12-31',
            },
          ],
        },
      ],
    },
    // Additional random entities
    {
      entityId: 'd1e2f3g4-h5i6-j7k8-l9m0-n1o2p3q4r5s6',
      entityName: 'MNO Corporate',
      dataReadinessStatus: DataReadinessStatus.VALIDATED_DATA,
      parentEntityId: '',
      periodId: 202301,
      startDate: '2023-01-01',
      endDate: '2023-12-31',
      children: [
        {
          entityId: 't1u2v3w4-x5y6-z7a8-b9c0-d1e2f3g4h5i6',
          entityName: 'MNO Sales',
          dataReadinessStatus: DataReadinessStatus.NEEDS_REVIEW,
          parentEntityId: 'd1e2f3g4-h5i6-j7k8-l9m0-n1o2p3q4r5s6',
          periodId: 202301,
          startDate: '2023-01-01',
          endDate: '2023-12-31',
          children: [
            {
              entityId: 'j1k2l3m4-n5o6-p7q8-r9s0-t1u2v3w4x5y6',
              entityName: 'MNO Sales East',
              dataReadinessStatus: DataReadinessStatus.NOT_READY,
              parentEntityId: 't1u2v3w4-x5y6-z7a8-b9c0-d1e2f3g4h5i6',
              periodId: 202301,
              startDate: '2023-01-01',
              endDate: '2023-12-31',
            },
            {
              entityId: 'k1l2m3n4-o5p6-q7r8-s9t0-u1v2w3x4y5z6',
              entityName: 'MNO Sales West',
              dataReadinessStatus: DataReadinessStatus.VALIDATED_DATA,
              parentEntityId: 't1u2v3w4-x5y6-z7a8-b9c0-d1e2f3g4h5i6',
              periodId: 202301,
              startDate: '2023-01-01',
              endDate: '2023-12-31',
            },
          ],
        },
      ],
    },
    {
      entityId: 'u1v2w3x4-y5z6-a7b8-c9d0-e1f2g3h4i5j6',
      entityName: 'PQR Corporate',
      dataReadinessStatus: DataReadinessStatus.NEEDS_REVIEW,
      parentEntityId: '',
      periodId: 202301,
      startDate: '2023-01-01',
      endDate: '2023-12-31',
      children: [
        {
          entityId: 'v1w2x3y4-z5a6-b7c8-d9e0-f1g2h3i4j5k6',
          entityName: 'PQR Sales',
          dataReadinessStatus: DataReadinessStatus.VALIDATED_DATA,
          parentEntityId: 'u1v2w3x4-y5z6-a7b8-c9d0-e1f2g3h4i5j6',
          periodId: 202301,
          startDate: '2023-01-01',
          endDate: '2023-12-31',
          children: [
            {
              entityId: 'w1x2y3z4-a5b6-c7d8-e9f0-g1h2i3j4k5l6',
              entityName: 'PQR Sales West',
              dataReadinessStatus: DataReadinessStatus.NEEDS_REVIEW,
              parentEntityId: 'v1w2x3y4-z5a6-b7c8-d9e0-f1g2h3i4j5k6',
              periodId: 202301,
              startDate: '2023-01-01',
              endDate: '2023-12-31',
              children: [],
            },
            {
              entityId: 'x1y2z3a4-b5c6-d7e8-f9g0-h1i2j3k4l5m6',
              entityName: 'PQR Sales East',
              dataReadinessStatus: DataReadinessStatus.NOT_READY,
              parentEntityId: 'v1w2x3y4-z5a6-b7c8-d9e0-f1g2h3i4j5k6',
              periodId: 202301,
              startDate: '2023-01-01',
              endDate: '2023-12-31',
              children: [],
            },
          ],
        },
      ],
    },
  ],
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/pages/data-readiness/data-source.ts`

```ts
import { api } from 'src/api/api';
import { RedirectResponse } from 'src/api/client';
import { resolve } from 'src/api/resolver';

const onError = (error: Error) => {
  window.console.error('Data Connections error', error);
  throw error;
};

export class DataReadinessDataSource {
  /**
   * Fetches Entity information.
   * @static
   * @async
   * @returns {EntityApiData}
   * @memberof DataReadinessDataSource
   */
  static async getEntity(startDate: string, endDate: string, periodId: string): Promise<unknown> {
    if (!startDate || !endDate || !periodId) {
      return;
    }

    const entityPromise = api.getEntities(startDate, endDate, periodId);
    if (!entityPromise) {
      throw new Error('Failed to fetch entity');
    }

    return resolve(entityPromise, (res: Response | RedirectResponse) => (res as Response).json(), onError);
  }

  /**
   * Fetches Entity details by entityId and startDate and endDate.
   * @static
   * @async
   * @returns {EntityApiData}
   * @memberof DataReadinessDataSource
   */
  static async getEntityByIdAndPeriod(
    startDate: string,
    endDate: string,
    entityId: string
  ): Promise<unknown> {
    if (!startDate || !endDate || !entityId) {
      return;
    }

    const entityPromise = api.getEntityByIdAndPeriod(startDate, endDate, entityId);
    if (!entityPromise) {
      throw new Error('Failed to fetch entity details');
    }

    return resolve(entityPromise, (res: Response | RedirectResponse) => (res as Response).json(), onError);
  }

  /**
   * Fetches Period config for tenant
   * @static
   * @async
   * @returns {FilingPeriodApiData}
   * @memberof DataReadinessDataSource
   */
  static async getPeriods(): Promise<unknown> {
    const periodPromise = api.getPeriods();
    if (!periodPromise) {
      throw new Error('Failed to fetch period data');
    }

    return resolve(periodPromise, (res: Response | RedirectResponse) => (res as Response).json(), onError);
  }

  /**
   * Fetches entity completeness data
   * @static
   * @async
   * @returns {EntityCompletenessApiData}
   * @memberof DataReadinessDataSource
   */
  static async getEntityCompleteness(startDate: string, endDate: string, entityId: string): Promise<unknown> {
    if (!startDate || !endDate || !entityId) {
      return;
    }

    const entityPromise = api.getEntityCompleteness(startDate, endDate, entityId);
    if (!entityPromise) {
      throw new Error('Failed to fetch entity completeness data');
    }

    return resolve(entityPromise, (res: Response | RedirectResponse) => (res as Response).json(), onError);
  }
}

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/components/breadcrumb/utils.ts`

```ts
import { BreadcrumbState, BreadcrumbStateWithDescriptor } from './types';

export const hasDescriptor = (
  breadcrumbState?: BreadcrumbState
): breadcrumbState is BreadcrumbStateWithDescriptor => !!breadcrumbState?.uri;

export const getLocationDescriptor = ({ state, uri }: BreadcrumbStateWithDescriptor) =>
  state ? { pathname: uri.toString(), state } : uri;

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/components/breadcrumb/hooks.ts`

```ts
import { useMemo } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

import { AbstractLocationState } from 'src/shared/types';
import { BreadcrumbState } from './types';
import { getLocationDescriptor, hasDescriptor } from './utils';

export const useBreadcrumbNavigation = () => {
  const navigate = useNavigate();
  const { state: locationState } = useLocation();
  const { breadcrumbStates } = locationState ?? {};

  const goBack = useMemo(() => {
    // @see https://www.typescriptlang.org/docs/handbook/2/functions.html#function-overloads
    function goBackStepsOrEvent(event: unknown): void;
    function goBackStepsOrEvent(steps?: number, breadcrumbLocationStateUpdate?: object): void;
    function goBackStepsOrEvent(
      /** Pass `number` in for more than one step back in browser history. */
      stepsOrEvent?: number | unknown,
      /** Updates to merge into the breadcrumb's location state object. */
      breadcrumbLocationStateUpdate?: object
    ) {
      const steps = typeof stepsOrEvent === 'number' ? stepsOrEvent : 1;
      const breadcrumbState = breadcrumbStates?.[breadcrumbStates.length - steps];

      if (breadcrumbState) {
        const updatedBreadcrumbState = breadcrumbLocationStateUpdate
          ? {
              ...breadcrumbState,
              state:
                typeof breadcrumbState?.state === 'object'
                  ? { ...breadcrumbState.state, ...breadcrumbLocationStateUpdate }
                  : breadcrumbLocationStateUpdate,
            }
          : breadcrumbState;

        if (hasDescriptor(updatedBreadcrumbState)) {
          navigate(getLocationDescriptor(updatedBreadcrumbState));
        }
      }
    }

    return goBackStepsOrEvent;
  }, [breadcrumbStates, navigate]);

  const goBackAndRefresh = useMemo(() => {
    // @see https://www.typescriptlang.org/docs/handbook/2/functions.html#function-overloads
    function goBackStepsOrEvent(event: unknown): void;
    function goBackStepsOrEvent(steps?: number, newBreadcrumbStates?: BreadcrumbState[]): void;
    function goBackStepsOrEvent(
      /** Pass `number` in for more than one step back in browser history. */
      stepsOrEvent?: number | unknown,
      /** Can be passed in to avoid issues with `history.replace` being async. */
      newBreadcrumbStates?: BreadcrumbState[]
    ) {
      const steps = typeof stepsOrEvent === 'number' ? stepsOrEvent : 1;
      const activeBreadcrumbStates = newBreadcrumbStates ?? breadcrumbStates;
      const breadcrumbState = activeBreadcrumbStates?.[activeBreadcrumbStates.length - steps];

      if (hasDescriptor(breadcrumbState)) {
        const { state, ...rest } = breadcrumbState;
        navigate(
          getLocationDescriptor({
            ...rest,
            state: {
              ...(typeof state === 'object' && state),
              pageLoadAction: 'REFRESH',
            },
          })
        );
      }
    }

    return goBackStepsOrEvent;
  }, [breadcrumbStates, navigate]);

  return {
    /**
     * Can be called directly or used as an event handler. Call with a `number` if more than one step back
     * in browser history is desired.
     */
    goBack,
    /**
     * Can be called directly or used as an event handler. Call with a `number` if more than one step back
     * in browser history is desired. Will also pass the REFRESH PageLoadAction
     */
    goBackAndRefresh,
  } as const;
};

export const useBreadcrumbs = <T extends AbstractLocationState>() => {
  const { state } = useLocation();
  const { breadcrumbStates } = state ?? {};

  return {
    breadcrumbStates,
    state,
  } as const;
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/components/breadcrumb/types.ts`

```ts
import { LocationDescriptor } from 'history';

import { IconType } from '@vertexinc/vtx-ui-react-component-library';

/**
 * @export
 * @interface BreadcrumbState
 */
export interface BreadcrumbState {
  icon?: IconType;
  state?: unknown;
  text: string;
  uri?: LocationDescriptor<unknown>;
}

export type BreadcrumbStateWithDescriptor = Omit<BreadcrumbState, 'uri'> & {
  uri: LocationDescriptor<unknown>;
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/components/filing-period-select/utils.ts`

```ts
import { FilingPeriod, FilingPeriodApiData, FilingPeriodSelectOption } from './types';

const formatDate = (isoDate: string | null): string => {
  if (!isoDate) return ''; // Return an empty string if the date is null or undefined
  // TODO: work on removing this string manipulation and use the ZonedDateTime library to parse the date
  // const defaultTimeZone = ZoneId.of('America/New_York'); // Set the default time zone to 'America/New_York'

  // console.log('isoDate', isoDate);
  // const zdt = ZonedDateTime.parse(isoDate).withZoneSameInstant(defaultTimeZone);

  // const day = zdt.dayOfMonth().toString();
  // const month = zdt.monthValue().toString().padStart(2, '0'); //
  // const year = zdt.year();

  const year = isoDate.substring(0, 4);
  const month = isoDate.substring(5, 7);
  const day = isoDate.substring(8, 10);
  return `${month}/${day}/${year}`;
};

export const formatFilingPeriod = (period: FilingPeriod): string => {
  return `${period.periodNumber} (${formatDate(period.startDate)} - ${formatDate(period.endDate)})`;
};

export const transformFilingPeriodsToSelectOptions = (
  data: FilingPeriodApiData
): FilingPeriodSelectOption[] => {
  const filingPeriods = data.periods as FilingPeriod[];

  return filingPeriods.map((period) => ({
    label: formatFilingPeriod(period),
    value: period.periodId.toString(),
    periodId: period.periodId,
    periodNumber: period.periodNumber,
    startDate: period.startDate,
    endDate: period.endDate,
    fiscalYear: period.fiscalYear,
  }));
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/components/filing-period-select/types.ts`

```ts
import { SelectOption } from 'src/shared/types';

export interface FilingPeriod {
  fiscalYear: number;
  periodNumber: number;
  periodId: string;
  startDate: string;
  endDate: string;
}

export interface FilingPeriodSelectOption extends SelectOption {
  fiscalYear: number;
  periodNumber: number;
  periodId: string;
  startDate: string;
  endDate: string;
}

export interface FilingPeriodApiData {
  periods: FilingPeriod[];
}

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/components/entity-table/utils.ts`

```ts
import { Entity, TableEntity } from './types';

const formatDate = (isoDate: string | null): string => {
  if (!isoDate) return ''; // Return an empty string if the date is null or undefined

  const year = isoDate.substring(0, 4);
  const month = isoDate.substring(5, 7);
  const day = isoDate.substring(8, 10);
  return `${month}/${day}/${year}`;
};

// Generate a numeric key for each entity
const generateNumericKey = (str: string, index: number) => {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = (hash << 5) - hash + str.charCodeAt(i);
    hash |= 0; // Convert to 32-bit integer
  }
  return Math.abs(hash) + index; // Ensure non-negative keys
};

// Transform the API data into the format needed for the grid
export const transformEntityData = (data: Entity, index: number): TableEntity => {
  const transformedData: TableEntity = {
    children: data.children?.length
      ? data.children
          .map((child, childIndex) => transformEntityData(child, childIndex))
          .sort((a, b) => a.entityName.localeCompare(b.entityName))
      : undefined,
    dataReadinessStatus: data.dataReadinessStatus,
    endDate: formatDate(data.endDate),
    entityName: data.entityName,
    entityId: data.entityId,
    key: generateNumericKey(String(data.entityId), index),
    periodId: data.periodId,
    parentEntityId: data.parentEntityId,
    startDate: formatDate(data.startDate),
  };

  return transformedData;
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/components/entity-table/types.ts`

```ts
import { DataReadinessStatus } from 'src/shared/constants-en';
import { FilingPeriodSelectOption } from '../filing-period-select/types';

export interface Entity {
  entityId: string;
  entityName: string;
  dataReadinessStatus: DataReadinessStatus;
  parentEntityId: string;
  periodId: number;
  startDate: string;
  endDate: string;
  children?: Entity[];
}

export interface EntityApiData {
  entityDataReadinessSummaries: Entity[];
}

export interface TableEntity extends Entity {
  key: number;
  children?: TableEntity[];
}

export enum EntityViewMode {
  RECONCILIATION = 'reconciliation',
  TAXABILITY = 'taxability',
  ADJUSTMENTS = 'adjustments',
  CLOSE_BOOKS = 'close-books',
}
export interface EntityTableContext {
  selectedPeriod: FilingPeriodSelectOption | null;
  entities: TableEntity[];
}

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/feature-flag/feature-flag-keys.ts`

```ts
import { IFeatureFlagClient as FeatureFlagClient } from '@vertexinc/vtx-ui-react-launchdarkly';

export type FeatureFlagMFE =
  | 'data-readiness-menu-item'
  | 'indirect-tax-close-menu-item'
  | 'data-files-menu-item'
  | 'datasets-menu-item'
  | 'source-systems-menu-item'
  | 'data-functions-menu-item'
  | 'enrichments-menu-item'
  | 'configuration-menu-item'
  | 'period-configuration-tab'
  | 'entity-configuration-tab'
  | 'maintenance-mode';

export type FeatureFlagName = FeatureFlagMFE;

export type IFeatureFlagClient = FeatureFlagClient<FeatureFlags>;

export type FeatureFlags = Record<FeatureFlagName, boolean>;

export const featureFlagDefaults: FeatureFlags = {
  'data-readiness-menu-item': false,
  'indirect-tax-close-menu-item': false,
  'data-files-menu-item': false,
  'datasets-menu-item': false,
  'source-systems-menu-item': false,
  'data-functions-menu-item': false,
  'enrichments-menu-item': false,
  'period-configuration-tab': false,
  'configuration-menu-item': false,
  'entity-configuration-tab': false,
  'maintenance-mode': false,
};

export type FeatureFlagDefaults = typeof featureFlagDefaults;

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/types/custom.d.ts`

```ts
declare module '*.svg' {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const content: any;
  // eslint-disable-next-line import/no-default-export
  export default content;
}

declare module '*.jpg' {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const content: any;
  // eslint-disable-next-line import/no-default-export
  export default content;
}

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/api/utils.ts`

```ts
/* eslint-disable import/prefer-default-export */

/**
 * A fallback that data sources can use to handle unexpected errors in their `resolve` calls.
 * Unlike the default `rejection` in the `resolve` it also creates a generic error
 * notification.  Ideally, this should eventually be handled consistently in one place.
 */
export const fallbackAPIErrorHandler = (error: Error) => {
  // eslint-disable-next-line no-console
  window.console.error('API error', error);
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/api/client.ts`

```ts
// import { VtxNotification } from '@vertexinc/vtx-ui-react-component-library';
import { getEnvVariable } from '../helpers/env-variables';
import { removeLeadingSlash, removeTrailingSlash } from '../helpers/utility';
import { HttpMethod } from './types';

export type ErrorObject = {
  errorId: string;
  messages?: string[];
  message?: string;
  timestamp: string;
  fieldName?: string;
};
export type QueryParamObject = {
  [key: string]: (string | number | boolean) | Array<string | number | boolean>;
};
export type RedirectResponse = {
  redirectUrl: string;
};

interface ClientParams<T> {
  uri: string;
  body?: BodyInit | Record<string, unknown> | T;
  method?: HttpMethod;
  headers?: Record<string, string>;
  pathParams?: Record<string, string>;
  queryParams?: QueryParamObject;
  suppressNotifications?: boolean;
  debug?: boolean;
  signal?: AbortSignal;
}

const baseUrl = getEnvVariable('API_BASE_URL');

interface AppliedHeaders {
  Authorization?: string;
  'Content-Type'?: string;
}

const getDefaultHeaders = (): AppliedHeaders => ({
  Authorization: `Bearer ${window.sessionStorage.getItem('access_token')}`,
  'Content-Type': 'application/json',
});

export const DEFAULT_ERROR_MESSAGE = 'There was an error processing your request. Please try again later.';

/**
 * Handles the response
 * @param response Response
 */
const handleResult = async (response: Response) => {
  if (response.redirected) {
    return {
      redirectUrl: response.url,
    } as RedirectResponse;
  }

  if (response.status >= 400) return response;

  try {
    return await response;
  } catch (error) {
    window.console.error('There was an error processing the request.', error);
    return response;
  }
};

export const replacePathParams = (url: string, pathParams?: Record<string, string>) => {
  const pathParamKeys = pathParams ? Object.keys(pathParams) : [];
  const warning = `${url} has path params that should be replaced via pathParams in your request.`;

  if (!url.match(/(:\w+)/)) return url;
  if (!pathParamKeys.length || !pathParams) {
    console.warn(warning); // eslint-disable-line no-console
    return url;
  }

  let updatedUrl = url;

  pathParamKeys.forEach((param: string) => {
    const regex = new RegExp(`:${param}`);
    updatedUrl = updatedUrl.replace(regex, encodeURIComponent(pathParams[param] as string));
  });

  if (updatedUrl.match(/(:\w+)/)) console.warn(warning); // eslint-disable-line no-console

  return updatedUrl;
};

export const expandArrayParams = (key: string, values: (string | number | boolean)[]) =>
  values.reduce(
    (accum, value, index: number) =>
      `${accum}${index ? '&' : ''}${encodeURIComponent(key)}=${encodeURIComponent(value)}`,
    ''
  );

export const appendQueryParams = (url: string, queryParams?: QueryParamObject) => {
  const queryParamKeys = queryParams ? Object.keys(queryParams) : [];
  let updatedUrl = url;

  if (!queryParamKeys.length || !queryParams) return url;

  queryParamKeys.forEach((param: string, index: number) => {
    const queryPartial = Array.isArray(queryParams[param])
      ? // eslint-disable-next-line @typescript-eslint/no-explicit-any
        expandArrayParams(param, queryParams[param] as any[])
      : `${encodeURIComponent(param)}=${encodeURIComponent(queryParams[param].toString())}`;
    updatedUrl = `${updatedUrl}${index ? '&' : '?'}${queryPartial}`;
  });

  return updatedUrl;
};

export const buildUrl = (
  url: string,
  pathParams?: Record<string, string>,
  queryParams?: QueryParamObject
) => {
  let updatedUrl = url;
  updatedUrl = replacePathParams(removeTrailingSlash(updatedUrl), pathParams);
  updatedUrl = appendQueryParams(updatedUrl, queryParams);

  return updatedUrl;
};

export const handleStatus = async (status: number, text: string, response: Response, suppress?: boolean) => {
  const message = (errorResponse: ErrorObject) => {
    switch (status) {
      case 400:
        return errorResponse.messages && errorResponse.messages.join('\n');
      case 401:
      case 403:
        return errorResponse.message;
      case 404:
        return 'The provided endpoint does not exist.';
      default:
        return 'The server was unable to process your request. Try again later.';
    }
  };

  if (status >= 400 && !response.redirected) {
    if ((response.headers.get('content-length') as unknown as number) <= 0) {
      const defaultErrorResponse = {
        errorId: '',
        timestamp: '',
        message: DEFAULT_ERROR_MESSAGE,
        messages: [DEFAULT_ERROR_MESSAGE],
      };

      if (!suppress) {
        // notification['error']({
        //   message: 'Error',
        //   description: message(defaultErrorResponse),
        // });
      }
      return Promise.reject(new Error(`${status}: ${text}\n${message(defaultErrorResponse)}`));
    }

    return response.json().then((errorResponse: ErrorObject) => {
      if (!suppress) {
        // notification['error']({
        //   message: 'Error',
        //   description: message(errorResponse),
        // });
      }
      // Forms have their own way of handling the errors as defined by UX, the errors
      // need to be associated with the fields for the form to be able to display the
      // field level validations. Therefore we should not form an error message if the
      // error response has field names in it.
      // The ideal error response should be an array of errors with error messages being
      // associated with the form fields. But we aren't getting that ATM, hence settling
      // for the fieldName (because, the backend fails out as soon it finds the first field
      // for which the validation fails)
      if (errorResponse.fieldName) {
        return Promise.reject(errorResponse);
      }
      return Promise.reject(new Error(`${status}: ${text}\n${message(errorResponse)}`));
    });
  }

  return response;
};

export const buildRequest = async <T>(params: ClientParams<T>) => {
  const { method = 'GET', uri, pathParams, queryParams, headers, body, debug, signal } = params;
  if (debug) {
    // eslint-disable-next-line no-console
    console.log('Client params:', params);
  }

  // `gc-ui` api methods use full URIs, but `ApiLinks` use relative URIs
  const url = uri.startsWith('http') ? uri : `${baseUrl}${removeLeadingSlash(uri)}`;
  const appliedHeaders = {
    ...getDefaultHeaders(),
    ...headers,
  };
  const bodyContents: BodyInit | Record<string, unknown> | T =
    appliedHeaders['Content-Type'] === 'multipart/form-data' && body ? body : JSON.stringify(body as T);

  /* We needed the content type to process things correctly, but now we want the browser to set it so we'll delete ours
   * https://muffinman.io/blog/uploading-files-using-fetch-multipart-form-data/ for more info */
  if (appliedHeaders['Content-Type'] && appliedHeaders['Content-Type'] === 'multipart/form-data') {
    delete appliedHeaders['Content-Type'];
  }

  return fetch(buildUrl(url, pathParams, queryParams), {
    method,
    signal,
    headers: appliedHeaders as HeadersInit,
    ...(!(['GET', 'DELETE'] as HttpMethod[]).includes(method) && {
      body: bodyContents as BodyInit,
    }),
  })
    .then((resp: Response) => handleStatus(resp.status, resp.statusText, resp, params.suppressNotifications))
    .then(async (resp: Response) => handleResult(resp));
};

export const client = {
  get: <T>(params: ClientParams<T>) => buildRequest({ method: 'GET', ...params }),
  put: <T>(params: ClientParams<T>) => buildRequest({ method: 'PUT', ...params }),
  post: <T>(params: ClientParams<T>) => buildRequest({ method: 'POST', ...params }),
  patch: <T>(params: ClientParams<T>) => buildRequest({ method: 'PATCH', ...params }),
  delete: <T>(params: ClientParams<T>) => buildRequest({ method: 'DELETE', ...params }),
} as const;

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/api/types.ts`

```ts
export type HttpMethod = 'GET' | 'PUT' | 'POST' | 'PATCH' | 'DELETE';

export type ApiDetails = {
  method: HttpMethod;
  href: string;
  accept: string;
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/api/api.ts`

```ts
// import { api as accuracyCurrentChangeApi } from './accuracy-risk/imposition/current/api';
import { api as menuApi } from './v1/menuitems/api';
import { api as userPermissionsApi } from './v1/user/permissions/api';
import { api as entitiesApi } from './v1/entity/api';
import { api as periodsApi } from './v1/period/api';

import { client } from './client';
export { DEFAULT_ERROR_MESSAGE } from './client';
export { fallbackAPIErrorHandler } from './utils';

/* Note to developers: please name the below entries according to
 * the endpoint name, not the function */

export const api = {
  /* Startup / Root */
  ...userPermissionsApi,
  ...menuApi,
  ...entitiesApi,
  ...periodsApi,

  fetch: (uri: string, headers: Record<string, string> = {}) =>
    client.get({
      uri,
      headers,
    }),
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/api/resolver.ts`

```ts
import { RedirectResponse } from './client';

type Resolver = (val: Response | RedirectResponse) => unknown;
type Rejector = (err: Error) => void;

const rejection = (error: Error) => window.console.error('Error resolving Promise', error); // eslint-disable-line no-console

export const resolve = async (
  execute: Promise<Response | RedirectResponse>,
  resolver: Resolver,
  reject: Rejector = rejection
) =>
  Promise.resolve(execute).then(
    (val) => resolver(val),
    (error: Error) => reject(error)
  );

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/api/v1/user/permissions/types.ts`

```ts
export type PermissionLevel = 'CREATE' | 'READ' | 'UPDATE' | 'DELETE';

export type UserPermissions = PermissionObject[];

export interface PermissionObject {
  dataTestId: string;
  permissionLevel: PermissionLevel;
}

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/api/v1/user/permissions/api.ts`

```ts
import { removeTrailingSlash } from '../../../../helpers/utility';
import { client } from '../../../client';
import { configBaseURL } from '../../../common/base-url';

const permissionUrl = `${removeTrailingSlash(configBaseURL)}/v1/user/permissions`;

export const api = {
  fetchUserPermissions: () =>
    client.get({
      uri: permissionUrl,
    }),
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/api/v1/entity/api.ts`

```ts
import { client } from 'src/api/client';
import { itcBaseURL } from 'src/api/common/base-url';
import { removeTrailingSlash } from 'src/helpers/utility';

const getEntityUrl = `${removeTrailingSlash(itcBaseURL)}/v1/data-readiness/entities`;
const getEntityByIdAndPeriodUrl = `${removeTrailingSlash(itcBaseURL)}/v1/data-readiness/entity`;
const getCompletenessUrl = `${removeTrailingSlash(itcBaseURL)}/v1/data-readiness/completeness`;

export const api = {
  getEntities: (startDate: string, endDate: string, periodId: string) => {
    return client.post({
      uri: getEntityUrl,
      body: {
        startDate,
        endDate,
        periodId,
      },
    });
  },
  getEntityByIdAndPeriod: (startDate: string, endDate: string, entityId: string) => {
    return client.post({
      uri: getEntityByIdAndPeriodUrl,
      body: {
        startDate,
        endDate,
        entityId,
      },
    });
  },
  getEntityCompleteness: (startDate: string, endDate: string, entityId: string) => {
    return client.post({
      uri: getCompletenessUrl,
      body: {
        startDate,
        endDate,
        entityId,
      },
    });
  },
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/api/v1/period/api.ts`

```ts
import { client } from 'src/api/client';
import { configBaseURL } from 'src/api/common/base-url';
import { removeTrailingSlash } from 'src/helpers/utility';

const getPeriodsUrl = `${removeTrailingSlash(configBaseURL)}/v1/period-configuration/tenant-periods`;

export const api = {
  getPeriods: () => {
    return client.get({
      uri: getPeriodsUrl,
    });
  },
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/api/v1/menuitems/api.ts`

```ts
import { removeTrailingSlash } from '../../../helpers/utility';
import { client } from '../../client';
import { configBaseURL } from '../../common/base-url';

const menuUrl = `${removeTrailingSlash(configBaseURL)}/v1/menuitems`;

export const api = {
  fetchMenu: () =>
    client.get({
      uri: menuUrl,
    }),
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/api/common/base-url.ts`

```ts
import { getEnvVariable } from 'src/helpers/env-variables';

export const configBaseURL = getEnvVariable('CONFIG_API_BASE_URL');
export const cloudBaseURL = getEnvVariable('CLOUD_API_BASE_URL');
export const itcBaseURL = getEnvVariable('ITC_API_BASE_URL');

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/shared/types.ts`

```ts
import { LocalDate } from '@vertexinc/vtx-ui-react-component-library';
import { BreadcrumbState } from '../components/breadcrumb/types';

export interface dateTypeForRangePicker {
  startDay: string;
  endDay: string;
}

export interface SelectOption {
  value: string;
  label: string;
  isDisabled?: boolean;
  isSelected?: boolean;
  isClearable?: boolean;
}

export type LocalTemporalRange = (LocalDate | null)[];

export type AbstractLocationState = {
  breadcrumbStates?: BreadcrumbState[];
  pageScrollPosition?: number;
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/shared/constants-en.ts`

```ts
export const CONSTANTS = {
  /**
   * This document contains the text for the entire MFE. PLEASE ADD A COMMENT when creating
   * a new section within this document so we can easily follow the use and location of these
   * elements without having to trace the code.
   */

  /* Maintinance Mode */
  MAINTENANCE_HEADING: 'Scheduled Maintenance',
  MAINTENANCE_MESSAGE: 'We are undergoing scheduled maintenance, please check back soon.',

  /* Data Readiness */
  COMPLETENESS_DESCRIPTION:
    'Use this section to compare metrics by tax category for data received in the previous and current filing periods with the percentage difference.',
  COMPLETENESS_TITLE: 'Completeness',
  DATA_READINESS_BREADCRUMB: 'Data Readiness',
  DATA_READINESS_NO_DATA_DESCRIPTION:
    'No tax close periods available, please configure data from configuration menu',
  DATA_READINESS_PAGE_DESCRIPTION:
    'This page displays the data readiness and tax close statuses for entities in the selected filing period. You can view the total list of entities, entities that need data reviewed, or entities moved to tax close.',
  DATA_READINESS_PAGE_HEADING: 'Data Readiness',
  DATA_READINESS_STATUS: 'Data Readiness',
  ENTITIES: 'Entities',
  ENTITY_NAME: 'Entities',
  ENTITY_PAGE_DESCRIPTION:
    'This page displays the details of the data readiness status for the selected entity and filing period. Details include metrics for quantity, quality, and completeness.',
  ENTITY_PAGE_NO_LOCATION_STATE: 'Please return to the Data Readiness page and select an entity.',
  FILING_PERIOD: 'Period',
  ITC_HEADING: 'Indirect Tax Close',
  SALES_DOLLAR: 'Sales (Dollar)',
  VIEW_DETAILS: 'View Details',
  NO_DATA: 'No Data',
  QUANTITY_TITLE: 'Quantity',
  QUANTITY_DESCRIPTION:
    'Use this section to review metrics for data sources, lines received, and transactions received.',
  TABS_ADJUSTMENTS: 'Adjustments',
  TABS_CLOSE_BOOKS: 'Close Books',
  TABS_RECONCILIATION: 'Reconciliation',
  TABS_TAXABILITY_REVIEW: 'Taxability Review',
  TAXABILITY_DESCRIPTION_1: 'This page displays all the available data views for',
  TAXABILITY_DESCRIPTION_2: 'for period',
  TAXABILITY_DESCRIPTION_3: 'You can also create custom data views here.',
  TAX_CLOSE_BREADCRUMB: 'Tax Close',
  TAX_CLOSE_PAGE_TITLE: 'Tax Close',
  TAX_CLOSE_STATUS_COLUMN_HEADER: 'Tax Close Status',
  TOTAL_LINES_RECEIVED: 'Total Lines Received',
  TOTAL_TRANSACTIONS_RECEIVED: 'Total Transactions Received',
  UNDERCONSTRUCTION_MESSAGE: 'This page is under construction',
  CONTEXT_HEADER_PREPARER: 'Preparer',
  CONTEXT_HEADER_PREPARER_NAME: 'Joan Smith',

  /* Generic */
  FOR: 'for',
  ON: 'on',

  ZERO: 'Zero',
  ONE: 'One',
  TWO: 'Two',
  THREE: 'Three',
  FOUR: 'Four',
  FIVE: 'Five',

  /* Basics */
  SAVE: 'Save',
  CANCEL: 'Cancel',
  OK: 'OK',

  /* Months */
  MONTHLY: 'Monthly',
  MONTH: 'Month',
  MONTH_JANUARY: 'January',
  MONTH_FEBRUARY: 'February',
  MONTH_MARCH: 'March',
  MONTH_APRIL: 'April',
  MONTH_MAY: 'May',
  MONTH_JUNE: 'June',
  MONTH_JULY: 'July',
  MONTH_AUGUST: 'August',
  MONTH_SEPTEMBER: 'September',
  MONTH_OCTOBER: 'October',
  MONTH_NOVEMBER: 'November',
  MONTH_DECEMBER: 'December',

  MONTH_JAN: 'Jan',
  MONTH_FEB: 'Feb',
  MONTH_MAR: 'Mar',
  MONTH_APR: 'Apr',
  MONTH_JUN: 'Jun',
  MONTH_JUL: 'Jul',
  MONTH_AUG: 'Aug',
  MONTH_SEP: 'Sep',
  MONTH_OCT: 'Oct',
  MONTH_NOV: 'Nov',
  MONTH_DEC: 'Dec',

  /* Entity Details Quality Metrics */
  LINES_SUCCESSFULLY_INGESTED: 'Lines Successfully Ingested',
  LINES_WITH_ERRORS: 'Lines with errors',
  QUALITY_TITLE: 'Quality',
  QUALITY_DESCRIPTION:
    'Use this section to review metrics for lines that are not standardized or validated, data that is missing from ingested lines, and data enrichment errors.',
  QUALITY_METRICS: 'Quality Metrics',
  TRANSACTIONS_SUCCESSFULLY_INGESTED: 'Transactions Successfully Ingested',
  VIEW_DATA_FILES: 'View Data Files',
};

export enum DataReadinessStatus {
  NOT_READY = 'Not Ready',
  NEEDS_REVIEW = 'Needs Review',
  VALIDATED_DATA = 'Validated Data',
}

export enum EntityCompletenessCategory {
  BASIS = 'Basis',
  TAX = 'Tax',
}

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/shared/data-test-id-map.ts`

```ts
export const DATA_TEST_ID = {
  _MENU_ITEM_HOME: 'home-menu-item',
  _MENU_ITEM_TAX_DATA: 'tax-data-menu-item',
  _MENU_ITEM_SOURCE_SYSTEMS: 'source-systems-menu-item',
  _MENU_ITEM_DATA_FILES: 'datasets-menu-item',
  _MENU_ITEM_DATA_SETS: 'data-files-menu-item',
  _MENU_ITEM_TRANSACTION_TAX_CLOSE: 'transaction-tax-close-menu-item',
  _MENU_ITEM_DATA_READINESS: 'data-readiness-menu-item',
  _MENU_ITEM_INDIRECT_TAX_CLOSE: 'indirect-tax-close-menu-item',
  _MENU_ITEM_LEDGERS_WORKBOOKS: 'ledgers-workbooks-menu-item',
  _MENU_ITEM_AUDIT_MANAGEMENT: 'audit-management-menu-item',
  _MENU_ITEM_TAX_PLANNING: 'tax-planning-menu-item',
  _MENU_ITEM_CONFIGURATION: 'configuration-menu-item',
  _MENU_ITEM_SETTINGS: 'settings-menu-item',
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/shared/custom-hooks/use-root.ts`

```ts
import { useContext } from 'react';
import { RootContext } from 'src/context/root-context';

export const useRootContext = () => {
  const context = useContext(RootContext);
  return context;
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/helpers/env-variables.ts`

```ts
export type WindowExtender = {
  API_BASE_URL: string;
  LAUNCH_DARKLY_CLIENT_ID: string;
};

declare const window: Window & WindowExtender;

export const getEnvVariable = (variable: string, defaultValue = ''): string =>
  (window[variable as keyof Window] as unknown as string) || process.env[`${variable}`] || defaultValue;

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/helpers/utility.ts`

```ts
/* eslint-disable @vertexinc/microfrontend/no-js-date */

import {
  convert,
  DateTimeFormatter,
  LocalDate,
  LocalDateTime,
  ZonedDateTime,
  ZoneId,
} from '@vertexinc/vtx-ui-react-component-library';
import { CONSTANTS } from 'src/shared/constants-en';
import { dateTypeForRangePicker, LocalTemporalRange } from '../shared/types';
import { Feature, Subscription } from '../types';
import { months } from '../utils/months-array';
import { HELPER_CONSTANTS } from './constants';

/**
 * Capitalize every letter in a string
 */
export const capitalizeAll = (str?: string | null) => str?.replace(/(^\w|\s\w)/g, (m) => m.toUpperCase());

/**
 * Convert the given string to title case
 * Ex: "SOUTH DAKOTA" --> "South Dakota"
 * Ex: "north dakota" --> "North Dakota"
 */
// Note: capitalizeAll needs to be renamed to something else. It can be easily confused with
// toUpperCase().
export const titleCase = (str?: string) => capitalizeAll(str?.toLowerCase()) as string;

/**
 * Capitalize only first letter in a string
 */
export const capitalizeFirstLetter = (str?: string) => str?.replace(/(^\w|\s)/g, (m) => m.toUpperCase());

/**
 * Removes any trailing slashes in the passed in uri.
 */
export const removeTrailingSlash = (uri: string) => uri.replace(/^(.+?)\/*?$/, '$1');

/**
 * Removes any leading slashes in the passed in uri.
 */
export const removeLeadingSlash = (uri: string) => uri.replace(/^\/+/, '');

/* #region URLS */
/** Returns a `string[]` if the query param is found in the given URL, or `null` if not. */
export const getQueryParamByName = (paramName: string, url: string): string[] | null => {
  // Inspired by https://stackoverflow.com/a/901144
  const values: string[] = [];
  const name = paramName.replace(/[[\]]/g, '\\$&');
  const regex = new RegExp(`[?&]${name}(=([^&#]*)|&|#|$)`, 'g');
  let results = regex.exec(url);

  while (results !== null) {
    if (!results[2]) {
      values.push('');
    } else {
      values.push(decodeURIComponent(results[2].replace(/\+/g, ' ')));
    }

    results = regex.exec(url);
  }

  return values.length ? values : null;
};

/**
 * Stable sort
 */
export const stableSort = (arr: unknown[], compare: (a: unknown, b: unknown) => number) =>
  arr
    .map((item, index) => ({ item, index }))
    .sort((a, b) => compare(a.item, b.item) || a.index - b.index)
    .map(({ item }) => item);

/**
 * Get last month's start and end date from the given/current date
 *
 * @return dateTypeForRangePicker
 */
export const getLastMonthStartEndDate = (
  format?: string,
  forDate?: string,
  minMax?: string
): dateTypeForRangePicker => {
  try {
    const dateInFormat = format ? format : 'yyyy-MM-dd';
    const date = forDate ? new Date(forDate) : new Date();

    // ISO string
    let startDate = new Date(date.getFullYear(), date.getMonth() - 1, 2).toISOString().slice(0, -1);
    //getting the last date of last month
    let endDate = new Date(date.getFullYear(), date.getMonth(), 1).toISOString().slice(0, -1);

    /**
     * Get specific starting/ending date of month.
     * min - to get dates according to minimum date range value
     * max - to get dates according to maximum date range value
     */
    if (minMax === 'min') {
      startDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() + 1)
        .toISOString()
        .slice(0, -1);
      endDate = new Date(date.getFullYear(), date.getMonth() + 1, 1).toISOString().slice(0, -1);
    } else if (minMax === 'max') {
      startDate = new Date(date.getFullYear(), date.getMonth(), 2).toISOString().slice(0, -1);
      endDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() + 1).toISOString().slice(0, -1);
    }

    const parsedStartDate = LocalDateTime.parse(startDate);
    const parsedEndDate = LocalDateTime.parse(endDate);

    const firstDay = parsedStartDate.format(DateTimeFormatter.ofPattern(dateInFormat));
    const lastDay = parsedEndDate.format(DateTimeFormatter.ofPattern(dateInFormat));

    const lastMonthDates = {
      startDay: firstDay,
      endDay: lastDay,
    };

    return lastMonthDates;
  } catch (err) {
    window.console.error('There was an error generating the last month start and end dates', err);
    return { startDay: '', endDay: '' };
  }
};

export const convertTextToDate = (dateString: string) => {
  try {
    const parsedDate = LocalDate.parse(dateString);
    return convert(parsedDate).toDate();
  } catch (err) {
    window.console.error('There was an error converting text to date', err);
    return null;
  }
};

export const convertTextToLocalDate = (dateString: string) => {
  try {
    return LocalDate.parse(dateString);
  } catch (err) {
    window.console.error('There was an error converting text to date', err);
    return null;
  }
};

/* Using an initial from date, return a range that includes the from date to the end of that month */
const returnPartialPriorLocalMonth = (from: LocalDate) => {
  try {
    const endDate = LocalDate.of(from.year(), from.month(), from.lengthOfMonth());
    return [from, endDate];
  } catch (err) {
    window.console.error('There was an error determining the prior month dates', err);
    return [];
  }
};

/* Using an initial to date, return the full range of the prior month */
export const returnMostRecentPriorMonth = (refDate: LocalDate) => {
  try {
    let startDate;
    if (refDate.month().value() === 1) {
      startDate = LocalDate.of(refDate.year() - 1, 12, 1);
    } else {
      startDate = LocalDate.of(refDate.year(), refDate.month().value() - 1, 1);
    }
    const endDate = LocalDate.of(startDate.year(), startDate.month(), startDate.lengthOfMonth());
    return [convert(startDate).toDate(), convert(endDate).toDate()];
  } catch (err) {
    window.console.error('There was an error determining the prior month dates', err);
    return [];
  }
};

/* Using an initial to date, return the full range of the prior month */
export const returnMostRecentPriorLocalMonth = (refDate: LocalDate) => {
  try {
    let startDate;
    if (refDate.month().value() === 1) {
      startDate = LocalDate.of(refDate.year() - 1, 12, 1);
    } else {
      startDate = LocalDate.of(refDate.year(), refDate.month().value() - 1, 1);
    }
    const endDate = LocalDate.of(startDate.year(), startDate.month(), startDate.lengthOfMonth());
    return [startDate, endDate];
  } catch (err) {
    window.console.error('There was an error determining the prior month dates', err);
    return [];
  }
};

export const differenceInMonths = (fromDate: LocalDate, toDate: LocalDate) => {
  try {
    return (toDate.year() - fromDate.year()) * 12 + (toDate.month().value() - fromDate.month().value());
  } catch (err) {
    window.console.error('There was an error determining the difference in months', err);
    return 0;
  }
};

export const insufficientDataInRange = (fromDate: string, toDate: string): boolean => {
  try {
    const earliestDate = LocalDate.parse(fromDate as string);
    const previousMonthDate = LocalDate.parse(toDate as string).minusMonths(1);
    const previousMonthStart = LocalDate.of(previousMonthDate.year(), previousMonthDate.month(), 1);
    return !(earliestDate.isBefore(previousMonthStart) || earliestDate.equals(previousMonthStart));
  } catch (err) {
    window.console.error('There was an error parsing the date range', err);
    return true;
  }
};

export const isDateValid = (dateString: string): boolean => {
  const validator = new RegExp(/^([\d]){2}[\/]([\d]){2}[\/]([\d]){4}$/);
  return validator.test(dateString);
};

/**
 * Examples for date picker (assume current date is July 20):
 *  a. Data is available from January 1st: show June 1-30 (entire previous month)
 *  b. Data is available from June 11th: Show June 11-30
 *  c. Data is available from July 4th: Show July 4-20
 *
 * @return TemporalRange
 */
export const getInitialSelectedLocalDates = (fromDate: string, toDate: string): LocalTemporalRange => {
  try {
    const localFrom = LocalDate.parse(fromDate);
    const localTo = LocalDate.parse(toDate);
    /* If both dates exist within the same year */
    if (localFrom.year() === localTo.year()) {
      /* If the dates live in the same month, return the dates */
      if (localFrom.month() === localTo.month()) {
        return [localFrom, localTo];
      } else if (localFrom.month().value() < localTo.month().value()) {
        if (localFrom.month().value() === localTo.month().value() - 1) {
          /* If the from date is the prior month, return that partial month */
          return returnPartialPriorLocalMonth(localFrom);
        } else if (localFrom.month().value() < localTo.month().value() - 1) {
          /* If the from date is more than one month from the to date, return
           * the last full month */
          return returnMostRecentPriorLocalMonth(localTo);
        }
      }
      /* If the from date is of a prior year */
    } else if (localFrom.year() < localTo.year()) {
      /* If the from date is the previous year */
      if (localFrom.year() === localTo.year() - 1) {
        /* Determine difference in months, for 1, return partial, for more, return prior */
        if (differenceInMonths(localFrom, localTo) > 1) {
          return returnMostRecentPriorLocalMonth(localTo);
        } else {
          return returnPartialPriorLocalMonth(localFrom);
        }
      } else if (localFrom.year() < localTo.year() - 1) {
        return returnMostRecentPriorLocalMonth(localTo);
      }
    }

    return [localFrom, localTo];
  } catch (err) {
    window.console.error('Error getting initial selected dates', err);
    return [];
  }
};

/**
 * Examples for date picker (assume current date is July 20):
 *  a. Data is available from January 1st: show June 1-30 (entire previous month)
 *  b. Data is available from June 11th: Show June 11-30
 *  c. Data is available from July 4th: Show July 4-20
 *
 * @return dateTypeForRangePicker
 */
export const getLastValidMonthStartEndDate = (
  minDate: string | null,
  maxDate: string | null,
  format?: string
): dateTypeForRangePicker => {
  const dateInFormat = format ? format : 'yyyy-MM-dd';
  const currentDate = new Date();
  const minDateRange = new Date(minDate || '');
  const maxDateRange = new Date(maxDate || '');

  let lastMonthDates = {
    startDay: '',
    endDay: '',
  };

  if (minDateRange.getFullYear() === maxDateRange.getFullYear()) {
    if (minDateRange.getMonth() === maxDateRange.getMonth()) {
      //when both dates are of same month return the dates
      lastMonthDates = {
        startDay: minDate || '',
        endDay: maxDate || '',
      };
    } else if (currentDate.getFullYear() > maxDateRange.getFullYear()) {
      // if data available for past year
      // min and max are consecutive months
      if (maxDateRange.getMonth() == minDateRange.getMonth() + 1) {
        lastMonthDates = getLastMonthStartEndDate(dateInFormat, maxDate || '', 'max'); //get dates from maxRange
      } else {
        lastMonthDates = getLastMonthStartEndDate(dateInFormat, maxDate || '');
      }
    } else if (
      currentDate.getMonth() > maxDateRange.getMonth() &&
      currentDate.getFullYear() === maxDateRange.getFullYear()
    ) {
      // min and max are consecutive months
      if (maxDateRange.getMonth() == minDateRange.getMonth() + 1) {
        lastMonthDates = getLastMonthStartEndDate(dateInFormat, maxDate || '', 'max'); //get dates from maxRange
      } else {
        lastMonthDates = getLastMonthStartEndDate(dateInFormat, maxDate || '');
      }
    } else if (
      currentDate.getMonth() == maxDateRange.getMonth() &&
      currentDate.getFullYear() === maxDateRange.getFullYear()
    ) {
      // min and max are consecutive months
      if (maxDateRange.getMonth() == minDateRange.getMonth() + 1) {
        lastMonthDates = getLastMonthStartEndDate(dateInFormat, minDate || '', 'min'); //get dates from minRange
      } else {
        lastMonthDates = getLastMonthStartEndDate(dateInFormat, maxDate || '');
      }
    }
  } else {
    //return last month from max date range
    lastMonthDates = getLastMonthStartEndDate(dateInFormat, maxDate || '');
  }

  return lastMonthDates;
};

type FormatterType = 'number' | 'percent' | 'currency';

const numberFormatter = new Intl.NumberFormat('en-US', {
  maximumFractionDigits: 2,
});

const percentFormatter = new Intl.NumberFormat('en-US', {
  style: 'percent',
  maximumFractionDigits: 2,
});

const currencyformatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  maximumFractionDigits: 2,
});

export const formatNumberToType = (amount: number | null, type: FormatterType) => {
  if (amount === null) {
    return numberFormatter.format(0);
  }
  switch (type) {
    case 'percent':
      return percentFormatter.format(amount / 100);
    case 'currency':
      return currencyformatter.format(amount);
    default:
      return numberFormatter.format(amount);
  }
};

export const monthList = [
  CONSTANTS.MONTH_JANUARY,
  CONSTANTS.MONTH_FEBRUARY,
  CONSTANTS.MONTH_MARCH,
  CONSTANTS.MONTH_APRIL,
  CONSTANTS.MONTH_MAY,
  CONSTANTS.MONTH_JUNE,
  CONSTANTS.MONTH_JULY,
  CONSTANTS.MONTH_AUGUST,
  CONSTANTS.MONTH_SEPTEMBER,
  CONSTANTS.MONTH_OCTOBER,
  CONSTANTS.MONTH_NOVEMBER,
  CONSTANTS.MONTH_DECEMBER,
];

const prependZero = (timeValue: number) => (timeValue < 10 ? `0${timeValue}` : timeValue);

/**
 * Takes a date string in the format listed below and converts it to ISO format
 * This method assumes the time is in UTC with no zone or offset designation
 *
 * @param dateString date value in the format of 'dd MM u hh:mm:ss a'
 */
export const getISODateFormat = (dateString: string) => {
  const dateSplit = dateString.split(' ');
  const dd = prependZero(Number(dateSplit[0]));
  const MM = prependZero(monthList.indexOf(dateSplit[1]) + 1);
  const u = dateSplit[2];
  const timeSplit = dateSplit[3].split(':');
  const hour =
    dateSplit[4] === 'AM'
      ? getHoursIn24HrFormat('AM', Number(timeSplit[0]))
      : getHoursIn24HrFormat('PM', Number(timeSplit[0]));
  const hh = hour < 10 ? prependZero(hour).toString() : hour.toString();
  const mm = prependZero(Number(timeSplit[1]));
  const ss = prependZero(Number(timeSplit[2]));
  const isoDateTimeUTC = `${u}-${MM}-${dd}T${hh}:${mm}:${ss}+00:00`;
  return isoDateTimeUTC;
};

const getHoursIn24HrFormat = (format: string, hours: number) => {
  if (format == 'PM' && hours < 12) hours = hours + 12;
  if (format == 'AM' && hours == 12) hours = hours - 12;
  return hours;
};

/**
 * Check if input dateString is valid ISO date
 * @param dateString input string
 * @returns boolean value if valid of not
 */
const isISOValid = (dateString: string) => /\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{1,}Z/.test(dateString);

/**
 * Takes a date string in the format listed below and converts to local time.
 * This method assumes that the original date is in UTC without the zone
 * designation, as our APIs currently return a time of unknown region/zone
 * without timezone or offset information included
 *
 * @param dateString date value in the format of 'dd MM u hh:mm:ss a'
 */
export const translateToLocal = (dateString: string | null) => {
  if (dateString) {
    if (!isISOValid(dateString)) return 'Unrecognized date format';
    try {
      const convertedDT = ZonedDateTime.parse(dateString).withZoneSameInstant(ZoneId.systemDefault());
      const dd = convertedDT.dayOfMonth();
      const MM = monthList[convertedDT.monthValue() - 1];
      const u = convertedDT.year();
      const hh = prependZero(convertedDT.hour());
      const mm = prependZero(convertedDT.minute());
      const ss = prependZero(convertedDT.second());
      /* Manually formatting here rather than using a formatter because it would
       * require we import the locale library which is huge, and we can instead use
       * the month list above to handle this for now. */
      const formattedDate = `${dd} ${MM} ${u} ${hh}:${mm}:${ss}`;
      return formattedDate;
    } catch (err) {
      return 'Unrecognized date format';
    }
  }
  return dateString;
};

/**
 * returns startDate and endDate in yyyy-mm-dd format of the given month and year
 * Ex:
 * Input : month -> October, year -> 2021
 * Output : startDate -> 2021-10-01, endDate -> 2021-10-31
 *
 * Ex:
 * Input : month -> February, year -> 2024
 * Output : startDate -> 2024-02-01, endDate -> 2024-02-29
 *
 * Ex:
 * Input : month -> February, year -> 2023
 * Output : startDate -> 2023-02-01, endDate -> 2023-02-28
 */
export const getFirstAndLastDateOfMonth = (
  month: string,
  year: string
): { startDate: string; endDate: string } => {
  const parsedYearInNumber = parseInt(year);
  const startMonthNumber = monthList.indexOf(month) + 1;
  const startDate = `${parsedYearInNumber}-${startMonthNumber <= 9 ? '0' : ''}${startMonthNumber}-01`;
  const nextMonthFromStartDate = `${startMonthNumber === 12 ? 1 + parsedYearInNumber : parsedYearInNumber}-${
    startMonthNumber === 12 ? '01' : startMonthNumber <= 8 ? `0${startMonthNumber + 1}` : startMonthNumber + 1
  }-01`;
  // 24 hrs * 60 mins * 60 seconds * 1000 milliseconds;
  const nextMonthMinusOneDay = new Date(new Date(nextMonthFromStartDate).getTime() - 24 * 60 * 60 * 1000);
  const endDate = `${nextMonthMinusOneDay.getFullYear()}-${
    (nextMonthMinusOneDay.getMonth() <= 8 ? `0` : ``) + (nextMonthMinusOneDay.getMonth() + 1)
  }-${(nextMonthMinusOneDay.getDate() <= 9 ? `0` : ``) + nextMonthMinusOneDay.getDate()}`;

  return { startDate, endDate };
};

/**
 * returns array of month range for given date range
 * Ex:
 * Input : fromDate -> new Date("05-05-2021"), toDate -> new Date("10-05-2021")
 * Output : ['May, 2021', 'June, 2021', 'July, 2021', 'August, 2021', 'September, 2021', 'October, 2021']
 */
export const getMonthRange = (fromDate: Date, toDate: Date) => {
  try {
    const monthRangeArray: string[] = [];

    // Calculating how many months are present between range
    const monthDiff = (dateFrom: Date, dateTo: Date) => {
      const to = new Date(dateTo);
      const from = new Date(dateFrom);
      return to.getMonth() - from.getMonth() + 12 * (to.getFullYear() - from.getFullYear());
    };

    const numberOfMonth = monthDiff(fromDate, toDate) + 1;

    // Getting start month and year
    const startDate = LocalDateTime.parse(new Date(fromDate).toISOString().slice(0, -1));
    let startMonth: number = parseInt(startDate.format(DateTimeFormatter.ofPattern('M')));
    let startYear: number = parseInt(startDate.format(DateTimeFormatter.ofPattern('yyyy')));

    for (let index = 0; index < numberOfMonth; index++) {
      if (startMonth === 13) {
        startMonth = 1;
        startYear = startYear + 1;
      }

      const result: string = monthList[startMonth - 1] + ', ' + startYear;
      startMonth++;

      monthRangeArray.push(result);
    }
    return monthRangeArray;
  } catch (err) {
    window.console.error('There was an error generating the month range', err);
    return [];
  }
};

export const formatNumericString = (value: string, type: FormatterType) => {
  try {
    const v = Number(value);
    if (isNaN(v)) {
      return value;
    } else {
      switch (type) {
        case 'number':
          return numberFormatter.format(v);
        case 'percent':
          return percentFormatter.format(v);
        case 'currency':
          return currencyformatter.format(v);
        default:
          return value;
      }
    }
  } catch (err) {
    window.console.error('There was an error formatting the date', err);
    return value;
  }
};

/* Calculate various time dimensions from millisecond values */
export const calcMinutesFromMilliseconds = (val: number): number => {
  return Math.floor(val / 60000);
};

export const calcHoursFromMilliseconds = (val: number): number => {
  return Math.floor(val / 3600000);
};

export const calcDaysFromMilliseconds = (val: number): number => {
  return Math.ceil(val / 86400000);
};

export const calcMonthsFromMilliseconds = (val: number): number => {
  return Math.floor(val / 2592000000);
};

export const getUpdateText = (diff: number): string => {
  /* Store the time values based on the difference of the lastUpdated time to now (system clock) */
  const calculatedMinutes = calcMinutesFromMilliseconds(diff);
  const calculatedHours = calcHoursFromMilliseconds(diff);
  const calculatedDays = calcDaysFromMilliseconds(diff);
  const calculatedMonths = calcMonthsFromMilliseconds(diff);

  if (diff < 60000) {
    return `${HELPER_CONSTANTS.LAST_UPDATED} ${HELPER_CONSTANTS.LESS_THAN_A_MINUTE}`;
  } else if (diff >= 60000 && diff < 3600000) {
    if (calculatedMinutes > 1) {
      return `${HELPER_CONSTANTS.LAST_UPDATED} ${calculatedMinutes} ${HELPER_CONSTANTS.MINUTES}`;
    } else {
      return `${HELPER_CONSTANTS.LAST_UPDATED} ${HELPER_CONSTANTS.MINUTE}`;
    }
  } else if (diff >= 3600000 && diff < 86400000) {
    if (calculatedHours > 1) {
      return `${HELPER_CONSTANTS.LAST_UPDATED} ${calculatedHours} ${HELPER_CONSTANTS.HOURS}`;
    } else {
      return `${HELPER_CONSTANTS.LAST_UPDATED} ${HELPER_CONSTANTS.HOUR}`;
    }
  } else if (diff >= 86400000 && diff < 2592000000) {
    if (calculatedDays > 1) {
      return `${HELPER_CONSTANTS.LAST_UPDATED} ${calculatedDays} ${HELPER_CONSTANTS.DAYS}`;
    } else {
      return `${HELPER_CONSTANTS.LAST_UPDATED} ${HELPER_CONSTANTS.DAY}`;
    }
  } else if (diff >= 2592000000) {
    if (calculatedMonths > 1) {
      return `${HELPER_CONSTANTS.LAST_UPDATED} ${HELPER_CONSTANTS.MONTHS}`;
    } else {
      return `${HELPER_CONSTANTS.LAST_UPDATED} ${HELPER_CONSTANTS.MONTH}`;
    }
  }
  return `${HELPER_CONSTANTS.LAST_UPDATED} ${HELPER_CONSTANTS.UNKNOWN}`;
};

export const disableDatesInPicker = (date: LocalDate, minDate: string, maxDate: string) => {
  try {
    if (date && minDate && maxDate) {
      const min = LocalDate.parse(minDate);
      const max = LocalDate.parse(maxDate);
      return date < min || date > max;
    }
    return false;
  } catch (err) {
    window.console.error('There was an errar disabling the dates', err);
    return false;
  }
};

export const checkSubscription = (sub: Subscription | null, code: string): boolean => {
  const subArray: string[] = [];
  sub?.features.map((feature: Feature, index: number) => {
    subArray.push(feature.featureCode);
  });
  return subArray.find((val: string) => val === code) === code;
};

/**
 * Returns first day of month derived from Month and year passed as paramenter.
 * for ex-  January,2022 will return 2022-01-01 in format YYYY-MM-DD
 * @param monthAndYear - in format January,2022
 */
export const getFirstDayOfMonthFromMonthAndYr = (monthAndYear: string) => {
  try {
    const splitText = monthAndYear.split(',');
    const month = splitText[0];
    const year = splitText[1];
    const monthNumber = monthList.indexOf(month) + 1;
    const firstDateForMonth = `${year}-${monthNumber <= 9 ? '0' : ''}${monthNumber}-01`;
    return firstDateForMonth.trim();
  } catch (err) {
    window.console.error('There was an error getting the first day and month', err);
    return '';
  }
};

/**
 * Get the table element from selector
 * @returns table scrollable element i.e tbody
 */
export const getTableContainer = (selector: string) => {
  const elem = document.querySelector(selector) as HTMLElement;
  return elem;
};

/**
 * Get scroll position of table
 * @returns scroll position
 */
export const getScrollPosition = (selector: string, callback: (scrollPos: number) => void) => {
  const tcontainer = getTableContainer(selector);
  const scrollPos = tcontainer ? tcontainer.scrollTop : 0;
  callback(scrollPos);
};

export const getDateInFormatYYYYMMDD = (inputDate: Date): string | undefined => {
  //return date in format YYYY-MM-DD
  if (isNaN(inputDate.getTime())) return;
  let month: string = inputDate.getMonth() + 1 + '';
  if (parseInt(month) <= 9) month = '0' + month;
  let date: string = inputDate.getDate() + '';
  if (parseInt(date) <= 9) date = '0' + date;
  const value = inputDate.getFullYear() + '-' + month + '-' + date;
  return value;
};

export const getParsedNumber = (number: string | number): number => {
  return parseInt(number.toString());
};

// return prior month of input date
// If input date = '01/01/2022' return - 'December, 2021'
export const getPriorMonthOfDate = (inputDate: LocalDate | undefined): string | undefined => {
  try {
    let startDate;
    if (inputDate && inputDate.month().value() === 1) {
      startDate = LocalDate.of(inputDate.year() - 1, 12, 1);
    } else {
      startDate = inputDate && LocalDate.of(inputDate.year(), inputDate.month().value() - 1, 1);
    }
    return startDate && monthList[startDate.month().value() - 1] + ', ' + startDate.year();
  } catch (err) {
    window.console.error('There was an error determining the prior month', err);
    return;
  }
};

export const sortNumberColumn = (x: number, y: number) => {
  if (isNaN(x) && isNaN(y)) {
    return 0;
  } else if (isNaN(x) && !isNaN(y)) {
    return -1;
  } else if (!isNaN(x) && isNaN(y)) {
    return 1;
  } else {
    return x - y;
  }
};

export const sortDateColumn = (d1: string, d2: string) => {
  const x = new Date(d1).getTime();
  const y = new Date(d2).getTime();
  if (isNaN(x) && isNaN(y)) {
    return 0;
  } else if (isNaN(x) && !isNaN(y)) {
    return -1;
  } else if (!isNaN(x) && isNaN(y)) {
    return 1;
  } else {
    return x - y;
  }
};

// get date in format 11 Jan 2022
// for invalid date return passed invalid value text
export const getDateInFormatDDMonthNameYYYY = (input: string, invalidText: string) => {
  let date;
  try {
    date = LocalDate.parse(input);
  } catch (e) {
    window.console.error('There was an error formatting the date', e);
    return invalidText;
  }
  const day = date.dayOfMonth() <= 9 ? '0' + date.dayOfMonth() : date.dayOfMonth();
  const d = `${date ? day + ' ' + months[date.monthValue() - 1] + ' ' + date.year() : invalidText}`;
  return d;
};

export const getDateInFormatMonYYYY = (input: string, invalidText: string) => {
  let date;
  try {
    date = LocalDate.parse(input);
  } catch (e) {
    window.console.error('There was an error formatting the date', e);
    return invalidText;
  }
  const d = `${date ? months[date.monthValue() - 1] + ' ' + date.year() : invalidText}`;
  return d;
};

export const getDateDifference = (dateUpdated: string | null) => {
  const updateDate = Date.parse(dateUpdated ? dateUpdated : '');
  const dateNow = Date.now();
  const dateDiff = dateNow - updateDate;
  return dateDiff;
};

export const convertStringToArray = (data: string | undefined) => {
  const output = data && data.split(',');
  return output;
};

export const arraysAreEqual = (arr1: unknown[], arr2: unknown[]) => {
  /* compare length */
  if (arr1.length !== arr2.length) return false;
  /* compare items */
  for (let i = 0; i < arr1.length; i++) {
    if (arr1[i] !== arr2[i]) return false;
  }
  return true;
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/helpers/utility.test.ts`

```ts
/* eslint-disable @vertexinc/microfrontend/no-js-date */
import { LocalDate } from '@vertexinc/vtx-ui-react-component-library';
import {
  convertStringToArray,
  differenceInMonths,
  getDateInFormatDDMonthNameYYYY,
  getDateInFormatYYYYMMDD,
  getInitialSelectedLocalDates,
  getISODateFormat,
  getPriorMonthOfDate,
  returnMostRecentPriorMonth,
  sortNumberColumn,
} from './utility';

const d = describe as unknown as jest.Describe;
const i = it as unknown as jest.It;
const e = expect as unknown as jest.Expect;

d('Return Prior Month Method', () => {
  i('Returns the correct dates when reference month is January', () => {
    const refDate = LocalDate.parse('2022-01-15');
    const priorMonth = returnMostRecentPriorMonth(refDate);
    e(priorMonth[0]?.getFullYear()).toEqual(2021);
    e(priorMonth[0]?.getMonth()).toEqual(11);
    e(priorMonth[0]?.getDate()).toEqual(1);
    e(priorMonth[1]?.getFullYear()).toEqual(2021);
    e(priorMonth[1]?.getMonth()).toEqual(11);
    e(priorMonth[1]?.getDate()).toEqual(31);
  });
  i('Returns the correct dates when reference month is February', () => {
    const refDate = LocalDate.parse('2022-02-15');
    const priorMonth = returnMostRecentPriorMonth(refDate);
    e(priorMonth[0]?.getFullYear()).toEqual(2022);
    e(priorMonth[0]?.getMonth()).toEqual(0);
    e(priorMonth[0]?.getDate()).toEqual(1);
    e(priorMonth[1]?.getFullYear()).toEqual(2022);
    e(priorMonth[1]?.getMonth()).toEqual(0);
    e(priorMonth[1]?.getDate()).toEqual(31);
  });
  i('Returns the correct dates when reference month is March', () => {
    const refDate = LocalDate.parse('2022-03-15');
    const priorMonth = returnMostRecentPriorMonth(refDate);
    e(priorMonth[0]?.getFullYear()).toEqual(2022);
    e(priorMonth[0]?.getMonth()).toEqual(1);
    e(priorMonth[0]?.getDate()).toEqual(1);
    e(priorMonth[1]?.getFullYear()).toEqual(2022);
    e(priorMonth[1]?.getMonth()).toEqual(1);
    e(priorMonth[1]?.getDate()).toEqual(28);
  });
  i('Returns the correct dates when reference month is April', () => {
    const refDate = LocalDate.parse('2022-04-15');
    const priorMonth = returnMostRecentPriorMonth(refDate);
    e(priorMonth[0]?.getFullYear()).toEqual(2022);
    e(priorMonth[0]?.getMonth()).toEqual(2);
    e(priorMonth[0]?.getDate()).toEqual(1);
    e(priorMonth[1]?.getFullYear()).toEqual(2022);
    e(priorMonth[1]?.getMonth()).toEqual(2);
    e(priorMonth[1]?.getDate()).toEqual(31);
  });
  i('Returns the correct dates when reference month is May', () => {
    const refDate = LocalDate.parse('2022-05-15');
    const priorMonth = returnMostRecentPriorMonth(refDate);
    e(priorMonth[0]?.getFullYear()).toEqual(2022);
    e(priorMonth[0]?.getMonth()).toEqual(3);
    e(priorMonth[0]?.getDate()).toEqual(1);
    e(priorMonth[1]?.getFullYear()).toEqual(2022);
    e(priorMonth[1]?.getMonth()).toEqual(3);
    e(priorMonth[1]?.getDate()).toEqual(30);
  });
  i('Returns the correct dates when reference month is June', () => {
    const refDate = LocalDate.parse('2022-06-15');
    const priorMonth = returnMostRecentPriorMonth(refDate);
    e(priorMonth[0]?.getFullYear()).toEqual(2022);
    e(priorMonth[0]?.getMonth()).toEqual(4);
    e(priorMonth[0]?.getDate()).toEqual(1);
    e(priorMonth[1]?.getFullYear()).toEqual(2022);
    e(priorMonth[1]?.getMonth()).toEqual(4);
    e(priorMonth[1]?.getDate()).toEqual(31);
  });
  i('Returns the correct dates when reference month is July', () => {
    const refDate = LocalDate.parse('2022-07-15');
    const priorMonth = returnMostRecentPriorMonth(refDate);
    e(priorMonth[0]?.getFullYear()).toEqual(2022);
    e(priorMonth[0]?.getMonth()).toEqual(5);
    e(priorMonth[0]?.getDate()).toEqual(1);
    e(priorMonth[1]?.getFullYear()).toEqual(2022);
    e(priorMonth[1]?.getMonth()).toEqual(5);
    e(priorMonth[1]?.getDate()).toEqual(30);
  });
  i('Returns the correct dates when reference month is August', () => {
    const refDate = LocalDate.parse('2022-08-15');
    const priorMonth = returnMostRecentPriorMonth(refDate);
    e(priorMonth[0]?.getFullYear()).toEqual(2022);
    e(priorMonth[0]?.getMonth()).toEqual(6);
    e(priorMonth[0]?.getDate()).toEqual(1);
    e(priorMonth[1]?.getFullYear()).toEqual(2022);
    e(priorMonth[1]?.getMonth()).toEqual(6);
    e(priorMonth[1]?.getDate()).toEqual(31);
  });
  i('Returns the correct dates when reference month is September', () => {
    const refDate = LocalDate.parse('2022-09-15');
    const priorMonth = returnMostRecentPriorMonth(refDate);
    e(priorMonth[0]?.getFullYear()).toEqual(2022);
    e(priorMonth[0]?.getMonth()).toEqual(7);
    e(priorMonth[0]?.getDate()).toEqual(1);
    e(priorMonth[1]?.getFullYear()).toEqual(2022);
    e(priorMonth[1]?.getMonth()).toEqual(7);
    e(priorMonth[1]?.getDate()).toEqual(31);
  });
  i('Returns the correct dates when reference month is October', () => {
    const refDate = LocalDate.parse('2022-10-15');
    const priorMonth = returnMostRecentPriorMonth(refDate);
    e(priorMonth[0]?.getFullYear()).toEqual(2022);
    e(priorMonth[0]?.getMonth()).toEqual(8);
    e(priorMonth[0]?.getDate()).toEqual(1);
    e(priorMonth[1]?.getFullYear()).toEqual(2022);
    e(priorMonth[1]?.getMonth()).toEqual(8);
    e(priorMonth[1]?.getDate()).toEqual(30);
  });
  i('Returns the correct dates when reference month is November', () => {
    const refDate = LocalDate.parse('2022-11-15');
    const priorMonth = returnMostRecentPriorMonth(refDate);
    e(priorMonth[0]?.getFullYear()).toEqual(2022);
    e(priorMonth[0]?.getMonth()).toEqual(9);
    e(priorMonth[0]?.getDate()).toEqual(1);
    e(priorMonth[1]?.getFullYear()).toEqual(2022);
    e(priorMonth[1]?.getMonth()).toEqual(9);
    e(priorMonth[1]?.getDate()).toEqual(31);
  });
  i('Returns the correct dates when reference month is December', () => {
    const refDate = LocalDate.parse('2022-12-15');
    const priorMonth = returnMostRecentPriorMonth(refDate);
    e(priorMonth[0]?.getFullYear()).toEqual(2022);
    e(priorMonth[0]?.getMonth()).toEqual(10);
    e(priorMonth[0]?.getDate()).toEqual(1);
    e(priorMonth[1]?.getFullYear()).toEqual(2022);
    e(priorMonth[1]?.getMonth()).toEqual(10);
    e(priorMonth[1]?.getDate()).toEqual(30);
  });
  i('Returns the correct dates for February in a Leap Year', () => {
    const refDate = LocalDate.parse('2020-03-15');
    const priorMonth = returnMostRecentPriorMonth(refDate);
    e(priorMonth[0]?.getFullYear()).toEqual(2020);
    e(priorMonth[0]?.getMonth()).toEqual(1);
    e(priorMonth[0]?.getDate()).toEqual(1);
    e(priorMonth[1]?.getFullYear()).toEqual(2020);
    e(priorMonth[1]?.getMonth()).toEqual(1);
    e(priorMonth[1]?.getDate()).toEqual(29);
  });
});

d('Difference in Months Method', () => {
  i('Returns the correct difference a month apart', () => {
    const fromDate = LocalDate.parse('2022-03-10');
    const toDate = LocalDate.parse('2022-04-25');
    const diff = differenceInMonths(fromDate, toDate);
    e(diff).toEqual(1);
  });
  i('Returns the correct difference two months apart', () => {
    const fromDate = LocalDate.parse('2022-03-10');
    const toDate = LocalDate.parse('2022-05-25');
    const diff = differenceInMonths(fromDate, toDate);
    e(diff).toEqual(2);
  });
  i('Returns the correct difference a month apart across years', () => {
    const fromDate = LocalDate.parse('2021-12-10');
    const toDate = LocalDate.parse('2022-01-25');
    const diff = differenceInMonths(fromDate, toDate);
    e(diff).toEqual(1);
  });
  i('Returns the correct difference two months apart across years', () => {
    const fromDate = LocalDate.parse('2021-11-22');
    const toDate = LocalDate.parse('2022-01-25');
    const diff = differenceInMonths(fromDate, toDate);
    e(diff).toEqual(2);
  });
  i('Returns the correct difference a year apart', () => {
    const fromDate = LocalDate.parse('2021-03-10');
    const toDate = LocalDate.parse('2022-03-25');
    const diff = differenceInMonths(fromDate, toDate);
    e(diff).toEqual(12);
  });
  i('Returns the correct difference two years apart', () => {
    const fromDate = LocalDate.parse('2020-03-10');
    const toDate = LocalDate.parse('2022-03-25');
    const diff = differenceInMonths(fromDate, toDate);
    e(diff).toEqual(24);
  });
});

d('Initial Date Selection Routines', () => {
  i('Returns the same dates when they exist in the same month', () => {
    const fromDate = '2022-03-10';
    const toDate = '2022-03-25';
    const dateRange = getInitialSelectedLocalDates(fromDate, toDate);
    e(dateRange[0]?.year()).toEqual(2022);
    e(dateRange[0]?.month().toString()).toEqual('MARCH');
    e(dateRange[0]?.dayOfMonth()).toEqual(10);
    e(dateRange[1]?.year()).toEqual(2022);
    e(dateRange[1]?.month().toString()).toEqual('MARCH');
    e(dateRange[1]?.dayOfMonth()).toEqual(25);
  });
  i('Returns partial month dates when range includes only some of the previous month', () => {
    const fromDate = '2022-02-15';
    const toDate = '2022-03-20';
    const dateRange = getInitialSelectedLocalDates(fromDate, toDate);
    e(dateRange[0]?.year()).toEqual(2022);
    e(dateRange[0]?.month().toString()).toEqual('FEBRUARY');
    e(dateRange[0]?.dayOfMonth()).toEqual(15);
    e(dateRange[1]?.year()).toEqual(2022);
    e(dateRange[1]?.month().toString()).toEqual('FEBRUARY');
    e(dateRange[1]?.dayOfMonth()).toEqual(28);
  });
  i('Returns the prior month when more than a month of data is available', () => {
    const fromDate = '2022-01-15';
    const toDate = '2022-04-20';
    const dateRange = getInitialSelectedLocalDates(fromDate, toDate);
    e(dateRange[0]?.year()).toEqual(2022);
    e(dateRange[0]?.month().toString()).toEqual('MARCH');
    e(dateRange[0]?.dayOfMonth()).toEqual(1);
    e(dateRange[1]?.year()).toEqual(2022);
    e(dateRange[1]?.month().toString()).toEqual('MARCH');
    e(dateRange[1]?.dayOfMonth()).toEqual(31);
  });
  i('Returns the prior month when from date starts on the first of that month', () => {
    const fromDate = '2022-01-01';
    const toDate = '2022-02-05';
    const dateRange = getInitialSelectedLocalDates(fromDate, toDate);
    e(dateRange[0]?.year()).toEqual(2022);
    e(dateRange[0]?.month().toString()).toEqual('JANUARY');
    e(dateRange[0]?.dayOfMonth()).toEqual(1);
    e(dateRange[1]?.year()).toEqual(2022);
    e(dateRange[1]?.month().toString()).toEqual('JANUARY');
    e(dateRange[1]?.dayOfMonth()).toEqual(31);
  });
  i('Returns the correct data when the dates cross a year boundary (prior month partial month)', () => {
    const fromDate = '2021-12-07';
    const toDate = '2022-01-05';
    const dateRange = getInitialSelectedLocalDates(fromDate, toDate);
    e(dateRange[0]?.year()).toEqual(2021);
    e(dateRange[0]?.month().toString()).toEqual('DECEMBER');
    e(dateRange[0]?.dayOfMonth()).toEqual(7);
    e(dateRange[1]?.year()).toEqual(2021);
    e(dateRange[1]?.month().toString()).toEqual('DECEMBER');
    e(dateRange[1]?.dayOfMonth()).toEqual(31);
  });
  i('Returns the correct data when the dates cross a year boundary (prior month full month)', () => {
    const fromDate = '2021-12-01';
    const toDate = '2022-01-05';
    const dateRange = getInitialSelectedLocalDates(fromDate, toDate);
    e(dateRange[0]?.year()).toEqual(2021);
    e(dateRange[0]?.month().toString()).toEqual('DECEMBER');
    e(dateRange[0]?.dayOfMonth()).toEqual(1);
    e(dateRange[1]?.year()).toEqual(2021);
    e(dateRange[1]?.month().toString()).toEqual('DECEMBER');
    e(dateRange[1]?.dayOfMonth()).toEqual(31);
  });
  i('Returns the correct data when the dates cross a year boundary (prior months)', () => {
    const fromDate = '2021-10-15';
    const toDate = '2022-01-05';
    const dateRange = getInitialSelectedLocalDates(fromDate, toDate);
    e(dateRange[0]?.year()).toEqual(2021);
    e(dateRange[0]?.month().toString()).toEqual('DECEMBER');
    e(dateRange[0]?.dayOfMonth()).toEqual(1);
    e(dateRange[1]?.year()).toEqual(2021);
    e(dateRange[1]?.month().toString()).toEqual('DECEMBER');
    e(dateRange[1]?.dayOfMonth()).toEqual(31);
  });
  i('Returns the correct data when the dates cross a year boundary (multiple years)', () => {
    const fromDate = '2020-10-15';
    const toDate = '2022-01-05';
    const dateRange = getInitialSelectedLocalDates(fromDate, toDate);
    e(dateRange[0]?.year()).toEqual(2021);
    e(dateRange[0]?.month().toString()).toEqual('DECEMBER');
    e(dateRange[0]?.dayOfMonth()).toEqual(1);
    e(dateRange[1]?.year()).toEqual(2021);
    e(dateRange[1]?.month().toString()).toEqual('DECEMBER');
    e(dateRange[1]?.dayOfMonth()).toEqual(31);
  });
});

d('Return Prior month in format `MMM,YYYY`', () => {
  i('Returns the correct prior month', () => {
    const fromDate = LocalDate.of(2022, 10, 1);
    const month = getPriorMonthOfDate(fromDate);
    e(month).toEqual('September, 2022');
  });
  i('Returns the empty string on invalid date', () => {
    const fromDate = undefined;
    const month = getPriorMonthOfDate(fromDate);
    e(month).toEqual(undefined);
  });
});

d('Return Date In YYYYMMDD Format ', () => {
  i('Returns the correct date in YYYYMMDD format', () => {
    const fromDate = new Date('October, 2022');
    const date = getDateInFormatYYYYMMDD(fromDate);
    e(date).toEqual('2022-10-01');
  });
  i('Returns the empty string on invalid date', () => {
    const fromDate = new Date('invalid date');
    const date = getDateInFormatYYYYMMDD(fromDate);
    e(date).toEqual(undefined);
  });
  i('Returns the correct date in YYYYMMDD format', () => {
    const fromDate = new Date('03-01-2022');
    const date = getDateInFormatYYYYMMDD(fromDate);
    e(date).toEqual('2022-03-01');
  });
});

d('Should Sort Columns for number ', () => {
  i('Returns difference of numbers', () => {
    const number = sortNumberColumn(1, 2);
    e(number).toEqual(-1);
  });
  i('Returns 1 if second number is NAN ', () => {
    const number = sortNumberColumn(1, Number('NAN'));
    e(number).toEqual(1);
  });
  i('Returns -1 if first number is NAN ', () => {
    const number = sortNumberColumn(Number('NAN'), 2);
    e(number).toEqual(-1);
  });
});

d('Should return date in DD MMM YYYY format ', () => {
  i('Returns date', () => {
    const number = getDateInFormatDDMonthNameYYYY('2022-07-03', 'invalid date');
    e(number).toEqual('03 Jul 2022');
  });
  i('Returns detault text if invalid date sent', () => {
    const number = getDateInFormatDDMonthNameYYYY('aaaacccc', 'invalid date');
    e(number).toEqual('invalid date');
  });
});

d('Returns proper ISO Date format', () => {
  i('Returns 2022-01-01T00:00:00+00:00', () => {
    const isoDate = getISODateFormat('1 January 2022 12:00:00 AM');
    e(isoDate).toEqual('2022-01-01T00:00:00+00:00');
  });
  i('Returns 2022-01-01T12:00:00+00:00', () => {
    const isoDate = getISODateFormat('1 January 2022 12:00:00 PM');
    e(isoDate).toEqual('2022-01-01T12:00:00+00:00');
  });
  i('Returns 2022-02-01T01:01:01+00:00', () => {
    const isoDate = getISODateFormat('1 February 2022 01:01:01 AM');
    e(isoDate).toEqual('2022-02-01T01:01:01+00:00');
  });
  i('Returns 2022-02-01T13:01:01+00:00', () => {
    const isoDate = getISODateFormat('1 February 2022 01:01:01 PM');
    e(isoDate).toEqual('2022-02-01T13:01:01+00:00');
  });
  i('Returns 2022-03-01T02:02:02+00:00', () => {
    const isoDate = getISODateFormat('1 March 2022 02:02:02 AM');
    e(isoDate).toEqual('2022-03-01T02:02:02+00:00');
  });
  i('Returns 2022-03-01T14:02:02+00:00', () => {
    const isoDate = getISODateFormat('1 March 2022 02:02:02 PM');
    e(isoDate).toEqual('2022-03-01T14:02:02+00:00');
  });
  i('Returns 2022-04-01T03:03:03+00:00', () => {
    const isoDate = getISODateFormat('1 April 2022 03:03:03 AM');
    e(isoDate).toEqual('2022-04-01T03:03:03+00:00');
  });
  i('Returns 2022-04-01T15:03:03+00:00', () => {
    const isoDate = getISODateFormat('1 April 2022 03:03:03 PM');
    e(isoDate).toEqual('2022-04-01T15:03:03+00:00');
  });
  i('Returns 2022-05-01T04:04:04+00:00', () => {
    const isoDate = getISODateFormat('1 May 2022 04:04:04 AM');
    e(isoDate).toEqual('2022-05-01T04:04:04+00:00');
  });
  i('Returns 2022-05-01T16:04:04+00:00', () => {
    const isoDate = getISODateFormat('1 May 2022 04:04:04 PM');
    e(isoDate).toEqual('2022-05-01T16:04:04+00:00');
  });
  i('Returns 2022-06-01T05:05:05+00:00', () => {
    const isoDate = getISODateFormat('1 June 2022 05:05:05 AM');
    e(isoDate).toEqual('2022-06-01T05:05:05+00:00');
  });
  i('Returns 2022-06-01T17:05:05+00:00', () => {
    const isoDate = getISODateFormat('1 June 2022 05:05:05 PM');
    e(isoDate).toEqual('2022-06-01T17:05:05+00:00');
  });
  i('Returns 2022-07-01T06:06:06+00:00', () => {
    const isoDate = getISODateFormat('1 July 2022 06:06:06 AM');
    e(isoDate).toEqual('2022-07-01T06:06:06+00:00');
  });
  i('Returns 2022-07-01T18:06:06+00:00', () => {
    const isoDate = getISODateFormat('1 July 2022 06:06:06 PM');
    e(isoDate).toEqual('2022-07-01T18:06:06+00:00');
  });
  i('Returns 2022-08-01T07:07:07+00:00', () => {
    const isoDate = getISODateFormat('1 August 2022 07:07:07 AM');
    e(isoDate).toEqual('2022-08-01T07:07:07+00:00');
  });
  i('Returns 2022-08-01T19:07:07+00:00', () => {
    const isoDate = getISODateFormat('1 August 2022 07:07:07 PM');
    e(isoDate).toEqual('2022-08-01T19:07:07+00:00');
  });
  i('Returns 2022-09-01T08:08:08+00:00', () => {
    const isoDate = getISODateFormat('1 September 2022 08:08:08 AM');
    e(isoDate).toEqual('2022-09-01T08:08:08+00:00');
  });
  i('Returns 2022-09-01T20:08:08+00:00', () => {
    const isoDate = getISODateFormat('1 September 2022 08:08:08 PM');
    e(isoDate).toEqual('2022-09-01T20:08:08+00:00');
  });
  i('Returns 2022-10-01T09:09:09+00:00', () => {
    const isoDate = getISODateFormat('1 October 2022 09:09:09 AM');
    e(isoDate).toEqual('2022-10-01T09:09:09+00:00');
  });
  i('Returns 2022-10-01T21:09:09+00:00', () => {
    const isoDate = getISODateFormat('1 October 2022 09:09:09 PM');
    e(isoDate).toEqual('2022-10-01T21:09:09+00:00');
  });
  i('Returns 2022-11-01T10:10:10+00:00', () => {
    const isoDate = getISODateFormat('1 November 2022 10:10:10 AM');
    e(isoDate).toEqual('2022-11-01T10:10:10+00:00');
  });
  i('Returns 2022-11-01T22:10:10+00:00', () => {
    const isoDate = getISODateFormat('1 November 2022 10:10:10 PM');
    e(isoDate).toEqual('2022-11-01T22:10:10+00:00');
  });
  i('Returns 2022-12-01T11:11:11+00:00', () => {
    const isoDate = getISODateFormat('1 December 2022 11:11:11 AM');
    e(isoDate).toEqual('2022-12-01T11:11:11+00:00');
  });
  i('Returns 2022-12-01T23:11:11+00:00', () => {
    const isoDate = getISODateFormat('1 December 2022 11:11:11 PM');
    e(isoDate).toEqual('2022-12-01T23:11:11+00:00');
  });
});

d('Returns Array of string on string split by , ', () => {
  i('Returns Array', () => {
    const arr = convertStringToArray('All,Alabama');
    e(arr).toEqual(['All', 'Alabama']);
  });
});

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/helpers/constants.ts`

```ts
export const HELPER_CONSTANTS = {
  LAST_UPDATED: 'Last updated',
  LESS_THAN_A_MINUTE: 'less than a minute ago',
  MINUTE: 'a minute ago',
  MINUTES: ' minutes ago',
  HOUR: 'an hour ago',
  HOURS: ' hours ago',
  DAY: 'a day ago',
  DAYS: ' days ago',
  MONTH: 'about a month ago',
  MONTHS: 'months ago',
  UNKNOWN: 'unknown',
};
export const DEFAULT_PAGE_SIZE = 20;

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/src/helpers/permissions.ts`

```ts
import { PermissionLevel, UserPermissions } from '../api/v1/user/permissions/types';

export const hasPermission = (
  permissions: UserPermissions = [],
  component: string,
  level: PermissionLevel
): boolean => {
  const result = permissions?.filter((item) => {
    return item.dataTestId === component && item.permissionLevel === level;
  });
  return !(result?.length === 0);
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/models/client.ts`

```ts
export interface IClient {
  clientName: string;
  isActiveClient: boolean;
  redirectUrl: string;
  tenantId: string;
}

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/support/index.ts`

```ts
import './commands';

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/support/commands.ts`

```ts
/// <reference types="cypress" />
/// <reference types="@testing-library/cypress" />

import '@testing-library/cypress/add-commands';
import { byTestId } from './helpers';

type GetOptions = Parameters<typeof cy.get>[1];

declare global {
  // eslint-disable-next-line @typescript-eslint/no-namespace
  namespace Cypress {
    interface Chainable {
      getByTestId(id: string, options?: GetOptions): Chainable<JQuery<HTMLElement>>;
    }
  }
}

// Automation custom commands inspired by
// https://docs.cypress.io/guides/references/best-practices.html#Real-World-Example
Cypress.Commands.add('getByTestId', (id: string, options: GetOptions) => {
  return cy.get(byTestId(id), options);
});

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/support/component.ts`

```ts
// ***********************************************************
// This example support/component.ts is processed and
// loaded automatically before your test files.
//
// This is a great place to put global configuration and
// behavior that modifies Cypress.
//
// You can change the location of this file or turn off
// automatically serving support files with the
// 'supportFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/configuration
// ***********************************************************

// Import commands.js using ES2015 syntax:
import './commands';

// Alternatively you can use CommonJS syntax:
// require('./commands')

import { mount } from 'cypress/react18';

// Augment the Cypress namespace to include type definitions for
// your custom command.
// Alternatively, can be defined in cypress/support/component.d.ts
// with a <reference path="./component" /> at the top of your spec.
declare global {
  /* eslint-disable @typescript-eslint/no-namespace */
  namespace Cypress {
    interface Chainable {
      mount: typeof mount;
    }
  }
  /* eslint-enable @typescript-eslint/no-namespace */
}

Cypress.Commands.add('mount', mount);

// Example use:
// cy.mount(<MyComponent />)

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/support/helpers.ts`

```ts
export const byTestId = (id: string) => `[data-testid="${id}"]`;

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/factories/entity.ts`

```ts
import { faker } from '@faker-js/faker';
import { makeFakeDataResponse, OverrideProps } from 'cypress/factories/overrides';
import { DataReadinessStatus } from 'src/shared/constants-en';
import { Entity, EntityApiData } from '../../src/pages/data-readiness/types';

type OwnProps = OverrideProps<Entity>;

export const makeFakeEntityResponse = ({
  count = 1,
  overrideAllWith,
  overrideArrayItems,
  overrideResponse,
}: OwnProps) => {
  const seedFunction = (depth = 0): Entity => ({
    children:
      depth < 2
        ? Array.from({ length: faker.number.int({ min: 1, max: 3 }) }, () => seedFunction(depth + 1))
        : [],
    dataReadinessStatus: faker.helpers.enumValue(DataReadinessStatus),
    endDate: faker.date.recent().toString(),
    entityId: faker.string.alphanumeric(5),
    entityName: faker.company.name(),
    parentEntityId: faker.string.alphanumeric(5),
    periodId: faker.number.int(5),
    startDate: faker.date.recent().toString(),
  });

  const entities = makeFakeDataResponse<Entity>({
    count,
    overrideAllWith,
    overrideArrayItems,
    overrideResponse,
    seedFunction,
  });

  const response: EntityApiData = {
    entityDataReadinessSummaries: entities as Entity[],
    ...overrideResponse,
    ...overrideArrayItems,
  };

  return response;
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/factories/subscription.ts`

```ts
import { mergePartially } from 'merge-partially';

interface Feature {
  platformProductCode: string;
  featureCode: string;
  featureName: string;
}

export interface ProfileResponse {
  subscription: {
    features: Feature[];
  };
  tenant: {
    type: 'Client' | 'Vertex';
    id: string;
    subType: string;
  };
}

export const makeFakeSubscriptionObject = (override?: Partial<ProfileResponse>): ProfileResponse => {
  return mergePartially.deep<ProfileResponse>(
    {
      subscription: {
        features: [],
      },
      tenant: {
        type: 'Client',
        id: 'fake_tenant_id',
        subType: 'SMB',
      },
    },
    override
  );
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/factories/entity-completeness.ts`

```ts
import { faker } from '@faker-js/faker';
import { makeFakeDataResponse, OverrideProps } from 'cypress/factories/overrides';
import { EntityCompletenessCategory } from 'src/shared/constants-en';
import { EntityCompletenessApiData, EntityCompletenessDetails } from '../../src/pages/data-readiness/types';

type OwnProps = OverrideProps<EntityCompletenessApiData>;

const formatDate = (isoDate: string | null): string => {
  if (!isoDate) return ''; // Return an empty string if the date is null or undefined
  // TODO: follow up on date formatting
  const year = isoDate.substring(0, 4);
  const month = isoDate.substring(5, 7);
  const day = isoDate.substring(8, 10);
  return `${month}/${day}/${year}`;
};

export const makeFakeEntityCompletenessResponse = ({
  count = 1,
  overrideAllWith,
  overrideArrayItems,
  overrideResponse,
}: OwnProps) => {
  // build sub-object array for EntityCompletenessDetails
  const entityDataCompletenessDetails: EntityCompletenessDetails = {
    [EntityCompletenessCategory.BASIS]: [
      {
        completenessCategory: EntityCompletenessCategory.BASIS,
        currentPeriodTotal: faker.number.int(2),
        differencePercentage: faker.number.int(2),
        previousPeriodTotal: faker.number.int(2),
      },
    ],
    [EntityCompletenessCategory.TAX]: [
      {
        completenessCategory: EntityCompletenessCategory.TAX,
        currentPeriodTotal: faker.number.int(2),
        differencePercentage: faker.number.int(2),
        previousPeriodTotal: faker.number.int(2),
      },
    ],
  };

  // build main response object
  const seedFunction = (): EntityCompletenessApiData => ({
    entityDataCompletenessDetails: entityDataCompletenessDetails as EntityCompletenessDetails,
    currentPeriodEndDate: formatDate(faker.date.past().toISOString()),
    currentPeriodStartDate: formatDate(faker.date.future().toISOString()),
    previousPeriodEndDate: formatDate(faker.date.past().toISOString()),
    previousPeriodStartDate: formatDate(faker.date.future().toISOString()),
    currentPeriodNumber: faker.number.int(12),
    previousPeriodNumber: faker.number.int(12),
  });

  const completeness = makeFakeDataResponse<EntityCompletenessApiData>({
    count,
    overrideAllWith,
    overrideArrayItems,
    overrideResponse,
    seedFunction: seedFunction,
  });

  // @ts-expect-error no undefined values are being passed, TODO figure out how to fix this
  const response: EntityCompletenessApiData = {
    ...(completeness as EntityCompletenessApiData),
    ...overrideResponse,
    ...overrideArrayItems,
  };

  return response;
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/factories/token.ts`

```ts
import { Instant } from '@vertexinc/vtx-ui-react-component-library';
import { mergePartially } from 'merge-partially';

export interface Token {
  access_token: string;
  expires_at: number;
  scope: string;
  token_type: string;
  profile?: {
    name?: string;
  };
}

export const makeFakeToken = (override?: Partial<Token>): Token => {
  const twentyMinsFromNow = Instant.now().toEpochMilli() + 20 * 60 * 1000;

  return mergePartially.shallow<Token>(
    {
      // The access token must be a valid JWT because it gets decoded
      access_token:
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaHR0cHM6Ly92ZXJ0ZXhpbmMuY29tL3BlcnNvbklkIjoiYWJjMTIzIiwiaWF0IjoxNTE2MjM5MDIyfQ.R3AI0hfkEQfP_Y9CUVRa9Bouf2AFxXG4mI5DHJT5Qc4',
      expires_at: twentyMinsFromNow,
      scope: 'openid profile offline_access',
      token_type: 'bearer',
    },
    override
  );
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/factories/menu.ts`

```ts
import { IFirstLevelMenuItem } from '@vertexinc/vtx-ui-cross-spa-events';

export const makeMenuResponseObject = (override?: Partial<IFirstLevelMenuItem[]>): IFirstLevelMenuItem[] => {
  const menu: IFirstLevelMenuItem[] = [
    {
      title: 'Home',
      dataTestId: 'home-menu-item',
      icon: {
        typeName: 'home',
      },
      linkUrl: '/ui/concourse/home',
    },
    {
      title: 'Tax Data',
      dataTestId: 'tax-data-menu-item',
      icon: {
        typeName: 'pie-chart',
      },
      children: [
        {
          title: 'Source Systems',
          dataTestId: 'source-systems-menu-item',
          linkUrl: '/ui/itc-data-ingestion/source-systems',
        },
        {
          title: 'Datasets',
          dataTestId: 'datasets-menu-item',
          linkUrl: '/ui/itc-data-ingestion/datasets',
        },
        {
          title: 'Data Files',
          dataTestId: 'data-files-menu-item',
          linkUrl: '/ui/itc-data-ingestion/data-files',
        },
        {
          title: 'Data Functions',
          dataTestId: 'data-functions-menu-item',
          children: [
            {
              title: 'Enrichments',
              dataTestId: 'enrichments-menu-item',
              linkUrl: '/ui/itc-data-ingestion/enrichments',
            },
          ],
        },
      ],
    },
    {
      title: 'Transaction Tax Close',
      dataTestId: 'transaction-tax-close-menu-item',
      icon: {
        typeName: 'schedule',
      },
      children: [
        {
          title: 'Data Readiness',
          dataTestId: 'data-readiness-menu-item',
          linkUrl: '/ui/transaction-tax-close/data-readiness',
        },
        {
          title: 'Indirect Tax Close',
          dataTestId: 'indirect-tax-close-menu-item',
          linkUrl: '/ui/transaction-tax-close/indirect-tax-close',
        },
        {
          title: 'Ledgers & Workbooks',
          dataTestId: 'ledgers-workbooks-menu-item',
          children: [],
        },
      ],
    },
    {
      title: 'Audit Management',
      dataTestId: 'audit-management-menu-item',
      icon: {
        typeName: 'audit',
      },
      linkUrl: '#',
    },
    {
      title: 'Tax Planning',
      dataTestId: 'tax-planning-menu-item',
      icon: {
        typeName: 'line-chart',
      },
      children: [],
    },
    {
      title: 'Configuration',
      dataTestId: 'configuration-menu-item',
      icon: {
        typeName: 'enterprise',
      },
      linkUrl: '/ui/concourse-config/',
    },
    {
      title: 'Settings',
      dataTestId: 'settings-menu-item',
      icon: {
        typeName: 'setting',
      },
      linkUrl: '#',
    },
  ];

  return menu;
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/factories/client.ts`

```ts
import { mergePartially } from 'merge-partially';
import { IClient } from '../models/client';

export function makeFakeClient(override?: Partial<IClient>): IClient {
  return mergePartially.shallow<IClient>(
    {
      clientName: 'Fake client',
      isActiveClient: false,
      redirectUrl: 'https://www.google.com',
      tenantId: 'd6d98b88-c866-4496-9bd4-de7ba48d0f52',
    },
    override
  );
}

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/factories/launchdarkly.ts`

```ts
import { mergePartially } from 'merge-partially';

export interface FeatureFlag {
  flagVersion: number;
  trackEvents: boolean;
  value: boolean | string;
  variation: number;
  version: number;
}

export const makeFakeFeatureFlag = (override?: Partial<FeatureFlag>): FeatureFlag => {
  return mergePartially.deep<FeatureFlag>(
    {
      flagVersion: 1,
      trackEvents: false,
      value: false,
      variation: 1,
      version: 1,
    },
    override
  );
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/factories/period.ts`

```ts
import { faker } from '@faker-js/faker';
import { makeFakeDataResponse, OverrideProps } from 'cypress/factories/overrides';
import { FilingPeriod, FilingPeriodApiData } from 'src/shared/components/filing-period-select/types';

type OwnProps = OverrideProps<FilingPeriod>;

const formatDate = (isoDate: string | null): string => {
  if (!isoDate) return ''; // Return an empty string if the date is null or undefined

  const year = isoDate.substring(0, 4);
  const month = isoDate.substring(5, 7);
  const day = isoDate.substring(8, 10);
  return `${month}/${day}/${year}`;
};

export const makeFakePeriodResponse = ({
  count = 1,
  overrideAllWith,
  overrideArrayItems,
  overrideResponse,
}: OwnProps) => {
  const seedFunction = (): FilingPeriod => ({
    fiscalYear: faker.date.future().getFullYear(),
    periodNumber: faker.number.int({ min: 1, max: 12 }),
    periodId: faker.number.int({ min: 1, max: 1000 }).toString(),
    startDate: formatDate(faker.date.past().toISOString()),
    endDate: formatDate(faker.date.future().toISOString()),
  });

  const periods = makeFakeDataResponse<FilingPeriod>({
    count,
    overrideAllWith,
    overrideArrayItems,
    seedFunction,
  });

  const response: FilingPeriodApiData = {
    periods: periods as FilingPeriod[],
    ...overrideResponse,
    ...overrideArrayItems,
  };

  return response;
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/factories/permissions.ts`

```ts
import { UserPermissions } from 'src/api/v1/user/permissions/types';
import { DATA_TEST_ID } from 'src/shared/data-test-id-map';

type UserRole = 'itc-admin' | 'itc-user';
const user: UserPermissions = [
  {
    dataTestId: `${DATA_TEST_ID._MENU_ITEM_HOME}`,
    permissionLevel: 'READ',
  },
  {
    dataTestId: `${DATA_TEST_ID._MENU_ITEM_TAX_DATA}`,
    permissionLevel: 'READ',
  },
  {
    dataTestId: `${DATA_TEST_ID._MENU_ITEM_SOURCE_SYSTEMS}`,
    permissionLevel: 'READ',
  },
  {
    dataTestId: `${DATA_TEST_ID._MENU_ITEM_SOURCE_SYSTEMS}`,
    permissionLevel: 'CREATE',
  },
  {
    dataTestId: `${DATA_TEST_ID._MENU_ITEM_DATA_FILES}`,
    permissionLevel: 'READ',
  },
  {
    dataTestId: `${DATA_TEST_ID._MENU_ITEM_DATA_SETS}`,
    permissionLevel: 'READ',
  },
  {
    dataTestId: `${DATA_TEST_ID._MENU_ITEM_DATA_SETS}`,
    permissionLevel: 'CREATE',
  },
  {
    dataTestId: `${DATA_TEST_ID._MENU_ITEM_TRANSACTION_TAX_CLOSE}`,
    permissionLevel: 'READ',
  },
  {
    dataTestId: `${DATA_TEST_ID._MENU_ITEM_DATA_READINESS}`,
    permissionLevel: 'READ',
  },
  {
    dataTestId: `${DATA_TEST_ID._MENU_ITEM_INDIRECT_TAX_CLOSE}`,
    permissionLevel: 'READ',
  },
  {
    dataTestId: `${DATA_TEST_ID._MENU_ITEM_LEDGERS_WORKBOOKS}`,
    permissionLevel: 'READ',
  },
  {
    dataTestId: `${DATA_TEST_ID._MENU_ITEM_AUDIT_MANAGEMENT}`,
    permissionLevel: 'READ',
  },
  {
    dataTestId: `${DATA_TEST_ID._MENU_ITEM_TAX_PLANNING}`,
    permissionLevel: 'READ',
  },
  {
    dataTestId: `${DATA_TEST_ID._MENU_ITEM_CONFIGURATION}`,
    permissionLevel: 'READ',
  },
  {
    dataTestId: `${DATA_TEST_ID._MENU_ITEM_SETTINGS}`,
    permissionLevel: 'READ',
  },
];

/*
 * As long as the admin account should always have the user permissions PLUS additional
 * permissions, we can start by reusing the user permissions and then add on top of them
 *
 * For now, we only have admin users, so eventually some of the user permissions will need
 * to be moved out into this admin array.
 */
const admin: UserPermissions = [...user];

export const makePermissionResponseObject = (
  role: UserRole | null,
  override: UserPermissions = []
): UserPermissions => {
  let permissions: UserPermissions = [];
  switch (role) {
    case 'itc-admin':
      permissions = admin;
      break;
    case 'itc-user':
      permissions = user;
    default:
      permissions = [];
  }
  return [...permissions, ...override];
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/factories/entity-details.ts`

```ts
import { faker } from '@faker-js/faker';
import { makeFakeDataResponse, OverrideProps } from 'cypress/factories/overrides';
import { DataReadinessStatus } from 'src/shared/constants-en';
import { EntityDetails } from '../../src/pages/data-readiness/types';

type OwnProps = OverrideProps<EntityDetails>;

export const makeFakeEntityDetailsResponse = ({
  count = 1,
  overrideAllWith,
  overrideArrayItems,
  overrideResponse,
}: OwnProps) => {
  const seedFunction = (): EntityDetails => ({
    dataReadiness: faker.helpers.enumValue(DataReadinessStatus),
    endDate: faker.date.recent().toString(),
    entityId: faker.string.alphanumeric(5),
    entityName: faker.company.name(),
    missingFieldLines: faker.number.int(2),
    notStandardizedLines: faker.number.int(2),
    notValidatedLines: faker.number.int(2),
    parentId: faker.number.int(2),
    periodId: faker.number.int(2),
    startDate: faker.date.recent().toString(),
    successfulLines: faker.number.int(2),
    successfulTransactions: faker.number.int(2),
    totalLines: faker.number.int(2),
    totalTransactions: faker.number.int(2),
  });

  const entityDetails = makeFakeDataResponse<EntityDetails>({
    count,
    overrideAllWith,
    overrideArrayItems,
    overrideResponse,
    seedFunction,
  });

  const response: EntityDetails = {
    ...(entityDetails as EntityDetails),
    ...overrideResponse,
    ...overrideArrayItems,
  };

  return response;
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/factories/overrides/index.ts`

```ts
import { mergePartially, NestedPartial } from 'merge-partially';

export type OverrideProps<T extends object> = {
  count?: number;
  /** Override all items in the array with this one */
  overrideAllWith?: NestedPartial<T>;
  /** Override certain elements in the array */
  overrideArrayItems?: NestedPartial<T>[];
  /** Override the response */
  overrideResponse?: NestedPartial<T>;
};

type LocalProps<T extends object> = OverrideProps<T> & {
  /** Seed function to create a fake object */
  seedFunction: () => NestedPartial<T>;
};

/**
 * Create a fake data response with { _data: T[], _links: {} }
 */
export const makeFakeDataResponse = <T extends object>({
  count = 1,
  overrideAllWith,
  overrideArrayItems = [],
  overrideResponse,
  seedFunction,
}: LocalProps<T>) => {
  const responseSeed = Array.from(
    { length: count },
    (_, index) =>
      mergePartially.deep(seedFunction() as object, {
        ...overrideArrayItems[index],
        ...overrideAllWith,
      }) as T
  );

  return overrideResponse ?? responseSeed;
  // TODO: need to understand mergePartially and arrays
  // return mergePartially.deep(responseSeed, overrideResponse);
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/mocked-api-routes/global-mocks.ts`

```ts
import { FeatureFlag } from 'cypress/factories/launchdarkly';
import { makeMenuResponseObject } from 'cypress/factories/menu';
import { makePermissionResponseObject } from 'cypress/factories/permissions';
import { setupAnalytics } from 'cypress/page-objects/analytics';
import { setClients } from 'cypress/page-objects/clients';
import { fakeFeatureFlags } from 'cypress/page-objects/feature-flags';
import { setupInternationalization } from 'cypress/page-objects/internationalization';
import { login } from 'cypress/page-objects/login';
import { setAppImportMapOverride } from 'cypress/page-objects/module-overrides';
import { setSubscriptions } from 'cypress/page-objects/subscriptions';
import { setupUserMonitoring } from 'cypress/page-objects/user-monitoring';
import { FeatureFlagMFE } from 'src/feature-flag/feature-flag-keys';
import { mockLaunchDarklyClientStreamGetRoute, mockLaunchDarklyGetRoute } from './launchdarkly';

interface InitGlobalMocksOptions {
  userPermissions?: ReturnType<typeof makePermissionResponseObject>;
  featureFlags?: Record<FeatureFlagMFE, FeatureFlag>;
}

export const initGlobalMocks = ({
  userPermissions = makePermissionResponseObject('itc-admin'),
  featureFlags = fakeFeatureFlags,
}: InitGlobalMocksOptions = {}) => {
  mockLaunchDarklyClientStreamGetRoute(featureFlags);
  mockLaunchDarklyGetRoute(featureFlags);
  cy.intercept('vtx-ui-mf-cnc-itc.js').as('mfeModule');
  cy.intercept('GET', '/v1/user/permissions', userPermissions).as('getUserPermissions');
  cy.intercept('GET', '/v1/menuitems', makeMenuResponseObject()).as('getMenuItems');
  login();
  setAppImportMapOverride();
  setSubscriptions();
  setClients();
  setupAnalytics();
  setupUserMonitoring();
  setupInternationalization();
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/mocked-api-routes/subscription.ts`

```ts
import { ProfileResponse } from '../factories/subscription';
import { routeAliases } from './route-aliases';

export const mockPlatformIntegrationProfileGetRoute = (response: ProfileResponse): void => {
  cy.intercept('GET', /platformintegration\/profile/, response).as(
    routeAliases.PlatformIntegrationProfileGet.ref
  );
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/mocked-api-routes/client.ts`

```ts
import { IClient } from '../models/client';
import { routeAliases } from './route-aliases';

export const mockClientsGetRoute = (response: IClient[]): void => {
  cy.intercept('GET', /\/site\/myuser\/clients/, response).as(routeAliases.ClientsGet.ref);
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/mocked-api-routes/launchdarkly.ts`

```ts
import { FeatureFlag } from '../factories/launchdarkly';
import { routeAliases } from './route-aliases';

// It is important to include the LD clientId in the route matcher to ensure we
// only intercept calls for the DMS/Concourse app's LD client.

export const mockLaunchDarklyGetRoute = (flags: { [name: string]: FeatureFlag }): void => {
  cy.intercept(/\/app.launchdarkly.com\/sdk\/evalx\/6717b4ade8898a083961dbd4/, {
    body: flags,
  }).as(routeAliases.LaunchDarklyGet.ref);
};

export const mockLaunchDarklyClientStreamGetRoute = (flags: { [name: string]: FeatureFlag }): void => {
  cy.intercept(/\/clientstream.launchdarkly.com\/eval\/6717b4ade8898a083961dbd4/, {
    body: flags,
    headers: { 'Content-Type': 'text/event-stream' },
  }).as(routeAliases.LaunchDarklyClientStreamGet.ref);
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/mocked-api-routes/route-aliases.ts`

```ts
export const routeAliases = getRouteAliases();

function getRouteAliases() {
  return Object.freeze({
    ClientsGet: {
      alias: '@clientsGet',
      ref: 'clientsGet',
    },
    PlatformIntegrationProfileGet: {
      alias: '@platformIntegrationProfileGet',
      ref: 'platformIntegrationProfileGet',
    },
    LaunchDarklyGet: {
      alias: '@launchDarklyGet',
      ref: 'launchDarklyGet',
    },
    LaunchDarklyClientStreamGet: {
      alias: '@launchDarklyClientStreamGet',
      ref: 'launchDarklyClientStreamGet',
    },
  });
}

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/integration/app-root/application-menu.spec.ts`

```ts
import { makeFakeEntityResponse } from 'cypress/factories/entity';
import { FeatureFlag, makeFakeFeatureFlag } from 'cypress/factories/launchdarkly';
import { makeFakePeriodResponse } from 'cypress/factories/period';
import { initGlobalMocks } from 'cypress/mocked-api-routes/global-mocks';
import { fakeFeatureFlags } from 'cypress/page-objects/feature-flags';
import { visitAndWait } from 'cypress/page-objects/visit-and-wait';
import { FeatureFlagMFE } from 'src/feature-flag/feature-flag-keys';
import { CONSTANTS } from 'src/shared/constants-en';

const dataReadinessFeatureFlags: Record<FeatureFlagMFE, FeatureFlag> = {
  ...fakeFeatureFlags,
  'data-readiness-menu-item': makeFakeFeatureFlag({ value: true }),
};

const interceptsForTests = () => {
  cy.intercept(
    'GET',
    '/v1/period-configuration/tenant-periods',
    makeFakePeriodResponse({
      count: 3,
    })
  ).as('periodResponse');
  cy.intercept(
    'POST',
    '/v1/data-readiness/entities',
    makeFakeEntityResponse({
      count: 3,
    })
  ).as('entityResponse');
};

const validateMenu = () => {
  cy.getByTestId('home-menu-item').should('exist');
  cy.getByTestId('tax-data-menu-item').should('exist');
  cy.getByTestId('source-systems-menu-item').should('exist');
  cy.getByTestId('datasets-menu-item').should('exist');
  cy.getByTestId('data-files-menu-item').should('exist');
  cy.getByTestId('data-functions-menu-item').should('exist');
  cy.getByTestId('enrichments-menu-item').should('exist');
  cy.getByTestId('transaction-tax-close-menu-item').should('exist');
  cy.getByTestId('data-readiness-menu-item').should('exist');
  cy.getByTestId('indirect-tax-close-menu-item').should('exist');
  cy.getByTestId('ledgers-workbooks-menu-item').should('exist');
  cy.getByTestId('audit-management-menu-item').should('exist');
  cy.getByTestId('tax-planning-menu-item').should('exist');
  cy.getByTestId('configuration-menu-item').should('exist');
  cy.getByTestId('settings-menu-item').should('exist');
};

describe('Application Menu', () => {
  beforeEach(() => {
    interceptsForTests();
    initGlobalMocks({ featureFlags: dataReadinessFeatureFlags });
  });

  it('Menu service is called and menu renders correctly', () => {
    visitAndWait('/data-readiness');
    cy.getByTestId('page-title').should('have.text', CONSTANTS.DATA_READINESS_PAGE_HEADING);
    cy.getByTestId('page-description').should('have.text', CONSTANTS.DATA_READINESS_PAGE_DESCRIPTION);
    validateMenu();
  });
});

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/integration/app-root/maintenance-mode.spec.ts`

```ts
import { makeFakeFeatureFlag } from 'cypress/factories/launchdarkly';
import { initGlobalMocks } from 'cypress/mocked-api-routes/global-mocks';
import { fakeFeatureFlags } from 'cypress/page-objects/feature-flags';
import { visitAndWait } from 'cypress/page-objects/visit-and-wait';
import { CONSTANTS } from 'src/shared/constants-en';

describe('Maintenance Mode', () => {
  const featureFlags = {
    ...fakeFeatureFlags,
    'maintenance-mode': makeFakeFeatureFlag({ value: true }),
  };
  beforeEach(() => {
    initGlobalMocks({ featureFlags: featureFlags });
  });

  it('Maintenence mode screen displays correctly when flag is engaged.', () => {
    visitAndWait('/');
    cy.get('h1').contains(CONSTANTS.MAINTENANCE_HEADING).should('exist');
    cy.get('p').contains(CONSTANTS.MAINTENANCE_MESSAGE).should('exist');
  });
});

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/integration/app-root/permissions.spec.ts`

```ts
import { makeFakeEntityResponse } from 'cypress/factories/entity';
import { FeatureFlag, makeFakeFeatureFlag } from 'cypress/factories/launchdarkly';
import { makeFakePeriodResponse } from 'cypress/factories/period';
import { makePermissionResponseObject } from 'cypress/factories/permissions';
import { initGlobalMocks } from 'cypress/mocked-api-routes/global-mocks';
import { fakeFeatureFlags } from 'cypress/page-objects/feature-flags';
import { visitAndWait } from 'cypress/page-objects/visit-and-wait';
import { UserPermissions } from 'src/api/v1/user/permissions/types';
import { FeatureFlagMFE } from 'src/feature-flag/feature-flag-keys';
import { CONSTANTS } from 'src/shared/constants-en';
import { DATA_TEST_ID } from 'src/shared/data-test-id-map';

const dataReadinessFeatureFlags: Record<FeatureFlagMFE, FeatureFlag> = {
  ...fakeFeatureFlags,
  'data-readiness-menu-item': makeFakeFeatureFlag({ value: true }),
};

const indirectTaxCloseFeatureFlags: Record<FeatureFlagMFE, FeatureFlag> = {
  ...fakeFeatureFlags,
  'indirect-tax-close-menu-item': makeFakeFeatureFlag({ value: true }),
};

const interceptsForTests = () => {
  cy.intercept(
    'GET',
    '/v1/period-configuration/tenant-periods',
    makeFakePeriodResponse({
      count: 3,
    })
  ).as('periodResponse');
  cy.intercept(
    'POST',
    '/v1/data-readiness/entities',
    makeFakeEntityResponse({
      count: 3,
    })
  ).as('entityResponse');
};

describe('Data Readiness Page - Permission Checks', () => {
  beforeEach(() => {
    interceptsForTests();
  });

  /* Data Readiness Page */
  it('Shows the Data Readiness page WITH READ permission and flag turned ON', () => {
    const permissionArray: UserPermissions = [
      {
        dataTestId: `${DATA_TEST_ID._MENU_ITEM_DATA_READINESS}`,
        permissionLevel: 'READ',
      },
    ];
    initGlobalMocks({
      userPermissions: makePermissionResponseObject('itc-admin', permissionArray),
      featureFlags: dataReadinessFeatureFlags,
    });
    visitAndWait('/data-readiness');
    cy.wait(3000);
    cy.get('[data-testid="page-title"]').contains(CONSTANTS.DATA_READINESS_PAGE_HEADING).should('exist');
  });

  it('Hides the Data Readiness page WITHOUT READ permission and flag turned ON', () => {
    const permissionArray: UserPermissions = [];
    initGlobalMocks({
      userPermissions: makePermissionResponseObject(null, permissionArray),
      featureFlags: dataReadinessFeatureFlags,
    });
    visitAndWait('/data-readiness');
    cy.wait(3000);
    cy.get('[data-testid="page-title"]').contains(CONSTANTS.DATA_READINESS_PAGE_HEADING).should('not.exist');
    cy.get('[data-testid="page-title"]').contains(CONSTANTS.ITC_HEADING).should('exist');
  });

  it('Hides the Data Readiness page WITH READ permission and flag turned OFF', () => {
    const permissionArray: UserPermissions = [
      {
        dataTestId: `${DATA_TEST_ID._MENU_ITEM_DATA_READINESS}`,
        permissionLevel: 'READ',
      },
    ];
    initGlobalMocks({
      userPermissions: makePermissionResponseObject('itc-admin', permissionArray),
      featureFlags: fakeFeatureFlags,
    });
    visitAndWait('/data-readiness');
    cy.wait(3000);
    cy.get('[data-testid="page-title"]').contains(CONSTANTS.DATA_READINESS_PAGE_HEADING).should('not.exist');
    cy.get('[data-testid="page-title"]').contains(CONSTANTS.ITC_HEADING).should('exist');
  });

  /* Indirect Tax Close Page */
  it('Shows the Indirect Tax Close page WITH READ permission and flag turned ON', () => {
    const permissionArray: UserPermissions = [
      {
        dataTestId: `${DATA_TEST_ID._MENU_ITEM_INDIRECT_TAX_CLOSE}`,
        permissionLevel: 'READ',
      },
    ];
    initGlobalMocks({
      userPermissions: makePermissionResponseObject('itc-admin', permissionArray),
      featureFlags: indirectTaxCloseFeatureFlags,
    });
    visitAndWait('/indirect-tax-close');
    cy.wait(3000);
    /* TODO: Update this test when actual page is available */
    cy.get('[data-testid="entities-heading"]').should('exist');
  });

  it('Hides the Indirect Tax Close page WITHOUT READ permission and flag turned ON', () => {
    const permissionArray: UserPermissions = [];
    initGlobalMocks({
      userPermissions: makePermissionResponseObject(null, permissionArray),
      featureFlags: indirectTaxCloseFeatureFlags,
    });
    visitAndWait('/indirect-tax-close');
    cy.wait(3000);
    /* TODO: Update this test when actual page is available */
    cy.get('[data-testid="entities-heading"]').should('not.exist');
    cy.get('[data-testid="page-title"]').contains(CONSTANTS.ITC_HEADING).should('exist');
  });

  it('Hides the Indirect Tax Close page WITH READ permission and flag turned OFF', () => {
    const permissionArray: UserPermissions = [
      {
        dataTestId: `${DATA_TEST_ID._MENU_ITEM_INDIRECT_TAX_CLOSE}`,
        permissionLevel: 'READ',
      },
    ];
    initGlobalMocks({
      userPermissions: makePermissionResponseObject('itc-admin', permissionArray),
      featureFlags: fakeFeatureFlags,
    });
    visitAndWait('/indirect-tax-close');
    cy.wait(3000);
    /* TODO: Update this test when actual page is available */
    cy.get('[data-testid="entities-heading"]').should('not.exist');
    cy.get('[data-testid="page-title"]').contains(CONSTANTS.ITC_HEADING).should('exist');
  });
});

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/integration/taxability/taxability.spec.ts`

```ts
import { makeFakeEntityResponse } from 'cypress/factories/entity';
import { FeatureFlag, makeFakeFeatureFlag } from 'cypress/factories/launchdarkly';
import { makeMenuResponseObject } from 'cypress/factories/menu';
import { makeFakePeriodResponse } from 'cypress/factories/period';
import { makePermissionResponseObject } from 'cypress/factories/permissions';
import { initGlobalMocks } from 'cypress/mocked-api-routes/global-mocks';
import { fakeFeatureFlags } from 'cypress/page-objects/feature-flags';
import { selectTabByLabel } from 'cypress/page-objects/tabs';
import { visitAndWait } from 'cypress/page-objects/visit-and-wait';
import { FeatureFlagMFE } from 'src/feature-flag/feature-flag-keys';
import { CONSTANTS, DataReadinessStatus } from 'src/shared/constants-en';

const featureFlags: Record<FeatureFlagMFE, FeatureFlag> = {
  ...fakeFeatureFlags,
  'indirect-tax-close-menu-item': makeFakeFeatureFlag({ value: true }),
};

const interceptsForTests = () => {
  cy.intercept('GET', '/v1/menuitems', makeMenuResponseObject()).as('getMenuItems');
  cy.intercept('GET', '/v1/user/permissions', makePermissionResponseObject('itc-admin')).as(
    'getUserPermissions'
  );
  cy.intercept('vtx-ui-mf-cnc-itc.js').as('mfeModule');
};

const TIME_TO_WAIT_FOR_BIG_FILES = 20000;

describe('Taxability page', () => {
  beforeEach(() => {
    initGlobalMocks({ featureFlags: featureFlags });
    interceptsForTests();
  });

  describe('View Taxability screen', () => {
    beforeEach(() => {
      cy.intercept(
        'GET',
        '/v1/period-configuration/tenant-periods',
        makeFakePeriodResponse({
          count: 3,
          overrideArrayItems: [
            {
              fiscalYear: 2024,
              periodNumber: 7,
              periodId: '1',
              startDate: '2024-07-01T00:00:00.000Z',
              endDate: '2024-07-31T00:00:00.000Z',
            },
            {
              fiscalYear: 2024,
              periodNumber: 6,
              periodId: '2',
              startDate: '2024-06-01T00:00:00.000Z',
              endDate: '2024-06-30T00:00:00.000Z',
            },
            {
              fiscalYear: 2024,
              periodNumber: 5,
              periodId: '3',
              startDate: '2024-05-01T00:00:00.000Z',
              endDate: '2024-05-31T00:00:00.000Z',
            },
          ],
        })
      ).as('periodResponse');

      cy.intercept(
        'POST',
        '/v1/data-readiness/entities',
        makeFakeEntityResponse({
          overrideArrayItems: [
            {
              entityName: 'A Entity',
              dataReadinessStatus: DataReadinessStatus.NEEDS_REVIEW,
              children: [
                {
                  entityName: 'B Entity',
                  dataReadinessStatus: DataReadinessStatus.NOT_READY,
                  children: [
                    {
                      entityName: 'C Entity',
                      dataReadinessStatus: DataReadinessStatus.VALIDATED_DATA,
                    },
                  ],
                },
              ],
            },
          ],
        })
      ).as('entityResponse');

      visitAndWait('/indirect-tax-close');
      cy.wait('@entityResponse', { timeout: TIME_TO_WAIT_FOR_BIG_FILES });
      cy.wait('@periodResponse');
    });

    it('Can navigate to Taxability screen', () => {
      cy.get('.ant-table-row-level-0')
        .first()
        .find('td')
        .first()
        .invoke('text')
        .then((text) => {
          const entityName = text;
          cy.get('.ant-table-row-level-0', {
            timeout: 10000,
          })
            .should('exist')
            .contains('A Entity')
            .click();

          // check for proper breadcrumb
          cy.getByTestId('breadcrumb-screen').should('have.text', entityName);
          // check for proper title
          cy.getByTestId('page-title').should('have.text', entityName);
          // check status pill
          cy.getByTestId('data-readiness-status').should('have.text', DataReadinessStatus.NEEDS_REVIEW);

          cy.getByTestId('context-header').should('exist');

          // Select taxability tab
          selectTabByLabel(CONSTANTS.TABS_TAXABILITY_REVIEW);

          // TSelect Taxability Review tab
          cy.get('[data-testid="tab-button-taxability"]').should('have.attr', 'aria-selected', 'true');

          // Test contents of the Taxability Review tab
          cy.get('[data-testid="tab-panel-taxability"]').within(($activeTab) => {
            const pageDescription = `${CONSTANTS.TAXABILITY_DESCRIPTION_1} ${entityName} ${CONSTANTS.TAXABILITY_DESCRIPTION_2} 7 (07/01/2024 - 07/31/2024). ${CONSTANTS.TAXABILITY_DESCRIPTION_3}`;
            cy.getByTestId('page-description').should('have.text', pageDescription);
          });

          // Navigate back to Tax Close page
          cy.getByTestId('breadcrumbs').findByRole('link', { name: CONSTANTS.TAX_CLOSE_BREADCRUMB }).click();
          cy.wait('@entityResponse', { timeout: TIME_TO_WAIT_FOR_BIG_FILES });
          cy.getByTestId('page-title').should('have.text', CONSTANTS.TAX_CLOSE_PAGE_TITLE);
        });
    });
  });
});

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/integration/indirect-tax-close/indirect-tax-close.spec.ts`

```ts
import { makeFakeEntityResponse } from 'cypress/factories/entity';
import { FeatureFlag, makeFakeFeatureFlag } from 'cypress/factories/launchdarkly';
import { makeFakePeriodResponse } from 'cypress/factories/period';
import { initGlobalMocks } from 'cypress/mocked-api-routes/global-mocks';
import { fakeFeatureFlags } from 'cypress/page-objects/feature-flags';
import {
  selectOptionIndexByAutomationId,
  selectPaginationResultsPerPageByValue,
} from 'cypress/page-objects/select';
import { visitAndWait } from 'cypress/page-objects/visit-and-wait';
import { FeatureFlagMFE } from 'src/feature-flag/feature-flag-keys';
import { CONSTANTS } from 'src/shared/constants-en';

const featureFlags: Record<FeatureFlagMFE, FeatureFlag> = {
  ...fakeFeatureFlags,
  'indirect-tax-close-menu-item': makeFakeFeatureFlag({ value: true }),
};

const TIME_TO_WAIT_FOR_BIG_FILES = 20000;
const interceptsForTests = () => {
  cy.intercept(
    'GET',
    '/v1/period-configuration/tenant-periods',
    makeFakePeriodResponse({
      count: 3,
      overrideArrayItems: [
        {
          fiscalYear: 2024,
          periodNumber: 7,
          periodId: '1',
          startDate: '2024-07-01T00:00:00.000Z',
          endDate: '2024-07-31T00:00:00.000Z',
        },
        {
          fiscalYear: 2024,
          periodNumber: 6,
          periodId: '2',
          startDate: '2024-06-01T00:00:00.000Z',
          endDate: '2024-06-30T00:00:00.000Z',
        },
        {
          fiscalYear: 2024,
          periodNumber: 5,
          periodId: '3',
          startDate: '2024-05-01T00:00:00.000Z',
          endDate: '2024-05-31T00:00:00.000Z',
        },
      ],
    })
  ).as('periodResponse');
};

describe('Indirect Tax Close', () => {
  describe('Table with no data', () => {
    beforeEach(() => {
      cy.intercept(
        'POST',
        '/v1/data-readiness/entities',
        makeFakeEntityResponse({
          count: 0,
        })
      ).as('entityResponse');
      interceptsForTests();
      initGlobalMocks({ featureFlags: featureFlags });
      visitAndWait('/indirect-tax-close');
      cy.wait('@periodResponse');
    });

    it('Indirect Tax Close page renders correctly', () => {
      cy.getByTestId('page-title').should('have.text', CONSTANTS.TAX_CLOSE_PAGE_TITLE);
      cy.getByTestId('context-header').should('exist');
      cy.get('[data-testid="entities-heading"]').should('have.text', CONSTANTS.ENTITIES);

      const expectedColumns = [
        { title: CONSTANTS.ENTITIES, hasSorter: true },
        { title: CONSTANTS.TAX_CLOSE_STATUS_COLUMN_HEADER, hasSorter: true },
      ];

      expectedColumns.forEach((column, index) => {
        cy.get('[data-testid="entity-table"] th').eq(index).should('contain.text', column.title);

        if (column.hasSorter) {
          cy.get('[data-testid="entity-table"] th')
            .eq(index)
            .find('.ant-table-column-sorters')
            .should('exist');
        } else {
          cy.get('[data-testid="entity-table"] th')
            .eq(index)
            .find('.ant-table-column-sorters')
            .should('not.exist');
        }
      });
      cy.get('[class="ant-empty-description"]').should('contain.text', 'No data');
      cy.get('.vtx-pagination__wrapper').should('exist');
      cy.getByTestId('vtx-pagination-button--previous').should('exist');
      cy.getByTestId('vtx-pagination-button--next').should('exist');
    });

    describe('Filing period select', () => {
      beforeEach(() => {
        cy.intercept(
          'POST',
          '/v1/data-readiness/entities',
          makeFakeEntityResponse({
            count: 4,
          })
        ).as('entityResponse');
        interceptsForTests();
        initGlobalMocks({ featureFlags: featureFlags });
        visitAndWait('/indirect-tax-close');
        cy.wait('@periodResponse');
      });

      it('Reloads page on period selection', () => {
        selectOptionIndexByAutomationId('select-filing-period-input', 2);
        cy.wait('@entityResponse');
        cy.getByTestId('select-filing-period-input').should('include.text', '5 (05/01/2024 - 05/31/2024)');
      });
    });
  });

  describe('Indirect Tax Close table with 100 rows of data', () => {
    beforeEach(() => {
      cy.intercept(
        'POST',
        '/v1/data-readiness/entities',
        makeFakeEntityResponse({
          count: 100,
        })
      ).as('entityResponse');
      interceptsForTests();
      initGlobalMocks({ featureFlags: featureFlags });
      visitAndWait('/indirect-tax-close');
      cy.wait('@periodResponse');
      cy.wait('@entityResponse', { timeout: TIME_TO_WAIT_FOR_BIG_FILES });
    });

    it('Shows proper pagination elements', () => {
      cy.get('.vtx-pagination__wrapper').should('exist');
      cy.getByTestId('button-target--10').should('exist');
      selectPaginationResultsPerPageByValue(100);
      cy.findByText('Showing 100 records.').should('exist');
    });
  });

  describe('Indirect Tax Close page with no filing periods', () => {
    describe('No period config data', () => {
      beforeEach(() => {
        cy.intercept(
          'POST',
          '/v1/data-readiness/entities',
          makeFakeEntityResponse({
            count: 4,
          })
        ).as('entityResponse');
        cy.intercept(
          'GET',
          '/v1/period-configuration/tenant-periods',
          makeFakePeriodResponse({
            count: 0,
          })
        ).as('periodResponse');
        initGlobalMocks({ featureFlags: featureFlags });
        visitAndWait('/indirect-tax-close');
      });

      it('Shows no data alert message', () => {
        cy.get('.vtx-alert-heading').should('contain.text', CONSTANTS.NO_DATA);
      });
    });
  });
});

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/integration/data-readiness/data-readiness-view-entity.spec.ts`

```ts
import { makeFakeEntityResponse } from 'cypress/factories/entity';
import { makeFakeEntityCompletenessResponse } from 'cypress/factories/entity-completeness';
import { makeFakeEntityDetailsResponse } from 'cypress/factories/entity-details';
import { FeatureFlag, makeFakeFeatureFlag } from 'cypress/factories/launchdarkly';
import { makeMenuResponseObject } from 'cypress/factories/menu';
import { makeFakePeriodResponse } from 'cypress/factories/period';
import { makePermissionResponseObject } from 'cypress/factories/permissions';
import { initGlobalMocks } from 'cypress/mocked-api-routes/global-mocks';
import { fakeFeatureFlags } from 'cypress/page-objects/feature-flags';
import { visitAndWait } from 'cypress/page-objects/visit-and-wait';
import { FeatureFlagMFE } from 'src/feature-flag/feature-flag-keys';
import { CONSTANTS, EntityCompletenessCategory } from 'src/shared/constants-en';

const dataReadinessFeatureFlags: Record<FeatureFlagMFE, FeatureFlag> = {
  ...fakeFeatureFlags,
  'data-readiness-menu-item': makeFakeFeatureFlag({ value: true }),
};

const interceptsForTests = () => {
  cy.intercept('GET', '/v1/menuitems', makeMenuResponseObject()).as('getMenuItems');
  cy.intercept('GET', '/v1/user/permissions', makePermissionResponseObject('itc-admin')).as(
    'getUserPermissions'
  );
  cy.intercept('vtx-ui-mf-cnc-itc.js').as('mfeModule');
};

const TIME_TO_WAIT_FOR_BIG_FILES = 20000;

describe('Data Readiness - View Entity Page', () => {
  beforeEach(() => {
    initGlobalMocks({ featureFlags: dataReadinessFeatureFlags });
    interceptsForTests();
  });

  describe('Navigate to Entity Details screen with bad entity id', () => {
    beforeEach(() => {
      visitAndWait('/data-readiness/entity/bad-entity-id');
    });

    it('Can handle bad or missing data', () => {
      cy.get('.vtx-alert-heading').should('contain.text', CONSTANTS.NO_DATA);
    });
  });

  describe('View Entity Details screen', () => {
    beforeEach(() => {
      cy.intercept(
        'GET',
        '/v1/period-configuration/tenant-periods',
        makeFakePeriodResponse({
          count: 3,
          overrideArrayItems: [
            {
              fiscalYear: 2024,
              periodNumber: 7,
              periodId: '1',
              startDate: '2024-07-01T00:00:00.000Z',
              endDate: '2024-07-31T00:00:00.000Z',
            },
            {
              fiscalYear: 2024,
              periodNumber: 6,
              periodId: '2',
              startDate: '2024-06-01T00:00:00.000Z',
              endDate: '2024-06-30T00:00:00.000Z',
            },
            {
              fiscalYear: 2024,
              periodNumber: 5,
              periodId: '3',
              startDate: '2024-05-01T00:00:00.000Z',
              endDate: '2024-05-31T00:00:00.000Z',
            },
          ],
        })
      ).as('periodResponse');

      cy.intercept(
        'POST',
        '/v1/data-readiness/entities',
        makeFakeEntityResponse({
          count: 3,
        })
      ).as('entityResponse');

      cy.intercept(
        'POST',
        '/v1/data-readiness/entity',
        makeFakeEntityDetailsResponse({
          count: 1,
          overrideResponse: {
            totalLinesCount: 1234,
            totalTransactionsCount: 5678,
            notStandardizedLines: 3,
            notValidatedLines: 3,
            missingFieldLines: 3,
            successfulLinesCount: 1225,
            successfulTransactionsCount: 5432,
          },
        })
      ).as('entityDetailsResponse');

      cy.intercept(
        'POST',
        '/v1/data-readiness/completeness',
        makeFakeEntityCompletenessResponse({
          count: 3,
          overrideResponse: {
            currentPeriodNumber: 3,
            currentPeriodStartDate: '2025-03-01T14:10:02.758Z',
            currentPeriodEndDate: '2025-03-31T14:10:02.758Z',
            previousPeriodNumber: 2,
            previousPeriodStartDate: '2025-02-01T14:10:02.758Z',
            previousPeriodEndDate: '2025-02-28T14:10:02.758Z',
            entityDataCompletenessDetails: {
              Basis: [
                {
                  completenessCategory: EntityCompletenessCategory.BASIS,
                  previousPeriodTotal: 4000342.0,
                  currentPeriodTotal: 3000342.0,
                  differencePercentage: 22.5,
                },
              ],
              Tax: [
                {
                  completenessCategory: EntityCompletenessCategory.TAX,
                  previousPeriodTotal: 260000.0,
                  currentPeriodTotal: 160000.0,
                  differencePercentage: 33.3,
                },
              ],
            },
          },
        })
      ).as('completenessResponse');

      visitAndWait('/data-readiness');
      cy.wait('@entityResponse', { timeout: TIME_TO_WAIT_FOR_BIG_FILES });
      cy.wait('@periodResponse');
    });

    it('Can view entity details screen', () => {
      cy.get('.ant-table-row-level-0')
        .first()
        .find('td')
        .first()
        .invoke('text')
        .then((text) => {
          const entityName = text;
          cy.get('.ant-table-row-level-0', {
            timeout: 10000,
          })
            .should('exist')
            .contains(CONSTANTS.VIEW_DETAILS)
            .click();
          // check for proper title
          cy.getByTestId('page-title').should('have.text', entityName);
          // check for proper breadcrumb
          cy.getByTestId('breadcrumb-screen').should('have.text', entityName);
        });

      // check for proper page elements
      cy.getByTestId('page-description').should('have.text', CONSTANTS.ENTITY_PAGE_DESCRIPTION);
      cy.findByLabelText(CONSTANTS.FILING_PERIOD).should('exist');

      //Quantity and section
      cy.log('Can view details Quantity section');

      cy.getByTestId('quantity-title').should('have.text', CONSTANTS.QUANTITY_TITLE);
      cy.getByTestId('quantity-description').should('have.text', CONSTANTS.QUANTITY_DESCRIPTION);

      cy.getByTestId('quantity-card-transactions')
        .find('.ant-card-head-title')
        .should('have.text', CONSTANTS.TOTAL_TRANSACTIONS_RECEIVED);
      cy.getByTestId('quantity-card-transactions').find('.ant-card-body').should('have.text', '5678');

      cy.getByTestId('quantity-card-lines')
        .find('.ant-card-head-title')
        .should('have.text', CONSTANTS.TOTAL_LINES_RECEIVED);
      cy.getByTestId('quantity-card-lines').find('.ant-card-body').should('have.text', '1234');
      // });

      // Quality section
      cy.log('Can view details Quality section');
      cy.getByTestId('quality-title').should('have.text', CONSTANTS.QUALITY_TITLE);
      cy.getByTestId('quality-description').should('have.text', CONSTANTS.QUALITY_DESCRIPTION);
      cy.getByTestId('view-data-files-link').should('have.text', CONSTANTS.VIEW_DATA_FILES);
      cy.getByTestId('successful-transactions').should('have.text', '5432');
      cy.getByTestId('successful-transactions-text').should(
        'have.text',
        CONSTANTS.TRANSACTIONS_SUCCESSFULLY_INGESTED
      );
      cy.getByTestId('successful-lines').should('have.text', '1225');
      cy.getByTestId('successful-lines-text').should('have.text', CONSTANTS.LINES_SUCCESSFULLY_INGESTED);
      cy.getByTestId('total-errors').should('have.text', '9');
      cy.getByTestId('errors-text').should('have.text', CONSTANTS.LINES_WITH_ERRORS);
      cy.getByTestId('errors-description').should(
        'have.text',
        '3 Lines not validated. 3 Lines not standardized. 3 Lines missing fields.'
      );

      // Completeness section
      cy.log('Can view details Completeness section');

      cy.wait('@completenessResponse', { timeout: TIME_TO_WAIT_FOR_BIG_FILES });
      cy.getByTestId('completeness-title').should('have.text', CONSTANTS.COMPLETENESS_TITLE);
      cy.getByTestId('completeness-description').should('have.text', CONSTANTS.COMPLETENESS_DESCRIPTION);

      const expectedColumns = [
        { title: 'Tax Category', hasSorter: false },
        { title: 'Period 2 (02/01/2025 - 02/28/2025)', hasSorter: false },
        { title: 'Period 3 (03/01/2025 - 03/31/2025)', hasSorter: false },
        { title: 'Difference', hasSorter: false },
      ];

      expectedColumns.forEach((column, index) => {
        cy.get('[data-testid="completeness-table"] th').eq(index).should('contain.text', column.title);
      });

      cy.get('[data-testid="completeness-table"] tbody tr')
        .eq(0)
        .find('td')
        .eq(1)
        .should('contain.text', '$4,000,342.00');

      cy.get('[data-testid="completeness-table"] tbody tr')
        .eq(1)
        .find('td')
        .eq(3)
        .should('contain.text', '(33.3)%');

      // navigate back to Data Readiness
      cy.getByTestId('breadcrumbs').findByRole('link', { name: CONSTANTS.DATA_READINESS_BREADCRUMB }).click();
      cy.wait('@entityResponse', { timeout: TIME_TO_WAIT_FOR_BIG_FILES });
      cy.getByTestId('page-title').should('have.text', CONSTANTS.DATA_READINESS_PAGE_HEADING);
    });
  });
});

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/integration/data-readiness/data-readiness.spec.ts`

```ts
import { makeFakeEntityResponse } from 'cypress/factories/entity';
import { FeatureFlag, makeFakeFeatureFlag } from 'cypress/factories/launchdarkly';
import { makeFakePeriodResponse } from 'cypress/factories/period';
import { initGlobalMocks } from 'cypress/mocked-api-routes/global-mocks';
import { fakeFeatureFlags } from 'cypress/page-objects/feature-flags';
import {
  selectOptionIndexByAutomationId,
  selectPaginationResultsPerPageByValue,
} from 'cypress/page-objects/select';
import { visitAndWait } from 'cypress/page-objects/visit-and-wait';
import { FeatureFlagMFE } from 'src/feature-flag/feature-flag-keys';
import { CONSTANTS, DataReadinessStatus } from 'src/shared/constants-en';

const dataReadinessFeatureFlags: Record<FeatureFlagMFE, FeatureFlag> = {
  ...fakeFeatureFlags,
  'data-readiness-menu-item': makeFakeFeatureFlag({ value: true }),
};

const TIME_TO_WAIT_FOR_BIG_FILES = 20000;

describe('Data Readiness Page', () => {
  const interceptsForTests = () => {
    cy.intercept(
      'GET',
      '/v1/period-configuration/tenant-periods',
      makeFakePeriodResponse({
        count: 3,
        overrideArrayItems: [
          {
            fiscalYear: 2024,
            periodNumber: 7,
            periodId: '1',
            startDate: '2024-07-01T00:00:00.000Z',
            endDate: '2024-07-31T00:00:00.000Z',
          },
          {
            fiscalYear: 2024,
            periodNumber: 6,
            periodId: '2',
            startDate: '2024-06-01T00:00:00.000Z',
            endDate: '2024-06-30T00:00:00.000Z',
          },
          {
            fiscalYear: 2024,
            periodNumber: 5,
            periodId: '3',
            startDate: '2024-05-01T00:00:00.000Z',
            endDate: '2024-05-31T00:00:00.000Z',
          },
        ],
      })
    ).as('periodResponse');
  };

  describe('Data Readiness', () => {
    describe('Filing period select', () => {
      beforeEach(() => {
        cy.intercept(
          'POST',
          '/v1/data-readiness/entities',
          makeFakeEntityResponse({
            count: 4,
          })
        ).as('entityResponse');
        interceptsForTests();
        initGlobalMocks({ featureFlags: dataReadinessFeatureFlags });
        visitAndWait('/data-readiness');
        cy.wait('@periodResponse');
      });

      it('Reloads page on period selection', () => {
        selectOptionIndexByAutomationId('select-filing-period-input', 2);
        cy.wait('@entityResponse');
        cy.getByTestId('select-filing-period-input').should('include.text', '5 (05/01/2024 - 05/31/2024)');
      });
    });

    describe('Table with no data', () => {
      beforeEach(() => {
        cy.intercept(
          'POST',
          '/v1/data-readiness/entities',
          makeFakeEntityResponse({
            count: 0,
          })
        ).as('entityResponse');
        interceptsForTests();
        initGlobalMocks({ featureFlags: dataReadinessFeatureFlags });
        visitAndWait('/data-readiness');
        cy.wait('@periodResponse');
      });

      it('Data Readiness page renders correctly', () => {
        cy.getByTestId('page-title').should('have.text', CONSTANTS.DATA_READINESS_PAGE_HEADING);
        cy.getByTestId('page-description').should('have.text', CONSTANTS.DATA_READINESS_PAGE_DESCRIPTION);
        cy.get('[data-testid="entities-heading"]').should('have.text', CONSTANTS.ENTITIES);

        const expectedColumns = [
          { title: 'Entities', hasSorter: true },
          { title: 'Data Readiness', hasSorter: true },
        ];

        expectedColumns.forEach((column, index) => {
          cy.get('[data-testid="entity-table"] th').eq(index).should('contain.text', column.title);

          if (column.hasSorter) {
            cy.get('[data-testid="entity-table"] th')
              .eq(index)
              .find('.ant-table-column-sorters')
              .should('exist');
          } else {
            cy.get('[data-testid="entity-table"] th')
              .eq(index)
              .find('.ant-table-column-sorters')
              .should('not.exist');
          }
        });
        cy.get('[class="ant-empty-description"]').should('contain.text', 'No data');
        cy.get('.vtx-pagination__wrapper').should('exist');
        cy.getByTestId('vtx-pagination-button--previous').should('exist');
        cy.getByTestId('vtx-pagination-button--next').should('exist');
      });
    });

    describe('Table with 100 rows of data', () => {
      beforeEach(() => {
        cy.intercept(
          'POST',
          '/v1/data-readiness/entities',
          makeFakeEntityResponse({
            count: 100,
          })
        ).as('entityResponse');
        interceptsForTests();
        initGlobalMocks({ featureFlags: dataReadinessFeatureFlags });
        visitAndWait('/data-readiness');
        cy.wait('@periodResponse');
        cy.wait('@entityResponse', { timeout: TIME_TO_WAIT_FOR_BIG_FILES });
      });

      it('Shows proper pagination elements', () => {
        cy.get('.vtx-pagination__wrapper').should('exist');
        cy.getByTestId('button-target--10').should('exist');
        selectPaginationResultsPerPageByValue(100);
        cy.findByText('Showing 100 records.').should('exist');
      });
    });

    describe('Table behaviour and characteristics', () => {
      beforeEach(() => {
        cy.intercept(
          'POST',
          '/v1/data-readiness/entities',
          makeFakeEntityResponse({
            count: 5,
          })
        ).as('entityResponse');
        interceptsForTests();
        initGlobalMocks({ featureFlags: dataReadinessFeatureFlags });
        visitAndWait('/data-readiness');
        cy.wait('@periodResponse');
        cy.wait('@entityResponse', { timeout: TIME_TO_WAIT_FOR_BIG_FILES });
      });

      it('Expands rows by default', () => {
        cy.get('.vtx-table-expand-icon:not(.vtx-table-expand-icon--hidden)').each(($button) => {
          cy.wrap($button).should('have.attr', 'aria-expanded', 'true');
        });
      });

      it('Expands and collapses rows', () => {
        cy.get('.vtx-table-expand-icon').first().click();
        cy.get('.vtx-table-expand-icon').first().should('have.attr', 'aria-expanded', 'false');
        cy.get('.vtx-table-expand-icon').first().click();
        cy.get('.vtx-table-expand-icon').first().should('have.attr', 'aria-expanded', 'true');
      });
    });

    describe('Table hierarchy', () => {
      beforeEach(() => {
        cy.intercept(
          'POST',
          '/v1/data-readiness/entities',
          makeFakeEntityResponse({
            overrideArrayItems: [
              {
                entityName: 'A Entity',
                dataReadinessStatus: DataReadinessStatus.NEEDS_REVIEW,
                children: [
                  {
                    entityName: 'B Entity',
                    dataReadinessStatus: DataReadinessStatus.NOT_READY,
                    children: [
                      {
                        entityName: 'C Entity',
                        dataReadinessStatus: DataReadinessStatus.VALIDATED_DATA,
                      },
                    ],
                  },
                ],
              },
            ],
          })
        ).as('entityResponse');
        interceptsForTests();
        initGlobalMocks({ featureFlags: dataReadinessFeatureFlags });
        visitAndWait('/data-readiness');
        cy.wait('@periodResponse');
        cy.wait('@entityResponse', { timeout: TIME_TO_WAIT_FOR_BIG_FILES });
      });

      it('Displays three levels for company, division and code', () => {
        // Check the first table cell of level 0
        cy.get('.ant-table-row-level-0')
          .first()
          .within(() => {
            cy.get('td').first().should('contain.text', 'A Entity');
          });

        // Check the first table cell of level 1
        cy.get('.ant-table-row-level-1')
          .first()
          .within(() => {
            cy.get('td').first().should('contain.text', 'B Entity');
          });

        // Check the first table cell of level 2
        cy.get('.ant-table-row-level-2')
          .first()
          .within(() => {
            cy.get('td').first().should('contain.text', 'C Entity');
          });
      });
    });

    describe('Table with sorting', () => {
      beforeEach(() => {
        cy.intercept(
          'POST',
          '/v1/data-readiness/entities',
          makeFakeEntityResponse({
            count: 3,
            overrideArrayItems: [
              {
                entityName: 'A Entity',
                dataReadinessStatus: DataReadinessStatus.NEEDS_REVIEW,
              },
              {
                entityName: 'B Entity',
                dataReadinessStatus: DataReadinessStatus.NOT_READY,
              },
              {
                entityName: 'C Entity',
                dataReadinessStatus: DataReadinessStatus.VALIDATED_DATA,
              },
            ],
          })
        ).as('entityResponse');
        interceptsForTests();
        initGlobalMocks({ featureFlags: dataReadinessFeatureFlags });
        visitAndWait('/data-readiness');
        cy.wait('@periodResponse');
        cy.wait('@entityResponse', { timeout: TIME_TO_WAIT_FOR_BIG_FILES });
      });

      it('Sorts properly', () => {
        // Sort Data Readiness column based on data in overrideArrayItems above
        // Ascending
        cy.get('.ant-table-column-sorters', { timeout: 10000 })
          .contains(CONSTANTS.DATA_READINESS_STATUS)
          .click({ force: true });
        cy.get('.ant-table-row-level-0', {
          timeout: 10000,
        })
          .should('exist')
          .contains(DataReadinessStatus.NEEDS_REVIEW);
        // Descending
        cy.get('.ant-table-column-sorters', { timeout: 10000 })
          .contains(CONSTANTS.DATA_READINESS_STATUS)
          .click({ force: true });
        cy.get('.ant-table-row-level-0', {
          timeout: 10000,
        })
          .should('exist')
          .contains(DataReadinessStatus.VALIDATED_DATA);

        // Sort Entities column based on data in overrideArrayItems above
        // Ascending
        cy.get('.ant-table-column-sorters', { timeout: 10000 })
          .contains(CONSTANTS.ENTITIES)
          .click({ force: true });
        cy.get('.ant-table-row-level-0', {
          timeout: 10000,
        })
          .should('exist')
          .contains('A Entity');
        // Descending
        cy.get('.ant-table-column-sorters', { timeout: 10000 })
          .contains(CONSTANTS.ENTITIES)
          .click({ force: true });
        cy.get('.ant-table-row-level-0', {
          timeout: 10000,
        })
          .should('exist')
          .contains('C Entity');
      });
    });

    describe('Table with status filtering', () => {
      beforeEach(() => {
        cy.intercept(
          'POST',
          '/v1/data-readiness/entities',
          makeFakeEntityResponse({
            count: 3,
            overrideArrayItems: [
              {
                entityName: 'A Entity',
                dataReadinessStatus: DataReadinessStatus.NEEDS_REVIEW,
                children: [],
              },
              {
                entityName: 'B Entity',
                dataReadinessStatus: DataReadinessStatus.NOT_READY,
                children: [],
              },
              {
                entityName: 'C Entity',
                dataReadinessStatus: DataReadinessStatus.VALIDATED_DATA,
                children: [],
              },
            ],
          })
        ).as('entityResponse');
        interceptsForTests();
        initGlobalMocks({ featureFlags: dataReadinessFeatureFlags });
        visitAndWait('/data-readiness');
        cy.wait('@periodResponse');
        cy.wait('@entityResponse', { timeout: TIME_TO_WAIT_FOR_BIG_FILES });
      });

      it('Filters by "Not Ready" status', () => {
        // Open the filter dropdown for the Data Readiness Status column
        cy.get('[data-testid="entity-table"] th').find('.ant-table-filter-trigger').eq(1).click();

        // Select the "Not Ready" filter
        cy.get('.ant-dropdown-menu-item').contains(DataReadinessStatus.NOT_READY).click();

        //Click OK
        cy.get('.ant-btn-primary').contains('OK').click();

        // Verify that only rows with "Not Ready" status are displayed
        cy.get('[data-testid="entity-table"] tbody tr').should('have.length', 1);
        cy.get('[data-testid="entity-table"] tbody tr')
          .first()
          .find('td')
          .first()
          .should('contain.text', 'B Entity');
        cy.get('[data-testid="entity-table"] tbody tr')
          .first()
          .find('td')
          .eq(1)
          .should('contain.text', DataReadinessStatus.NOT_READY);
      });

      it('Filters by "Needs Review" status', () => {
        cy.get('[data-testid="entity-table"] th').find('.ant-table-filter-trigger').eq(1).click();
        cy.get('.ant-dropdown-menu-item').contains(DataReadinessStatus.NEEDS_REVIEW).click();
        cy.get('.ant-btn-primary').contains('OK').click();
        cy.get('[data-testid="entity-table"] tbody tr').should('have.length', 1);
        cy.get('[data-testid="entity-table"] tbody tr')
          .first()
          .find('td')
          .first()
          .should('contain.text', 'A Entity');
        cy.get('[data-testid="entity-table"] tbody tr')
          .first()
          .find('td')
          .eq(1)
          .should('contain.text', DataReadinessStatus.NEEDS_REVIEW);
      });

      it('Filters by "Validated Data" status', () => {
        cy.get('[data-testid="entity-table"] th').find('.ant-table-filter-trigger').eq(1).click();
        cy.get('.ant-dropdown-menu-item').contains(DataReadinessStatus.VALIDATED_DATA).click();
        cy.get('.ant-btn-primary').contains('OK').click();
        cy.get('[data-testid="entity-table"] tbody tr').should('have.length', 1);
        cy.get('[data-testid="entity-table"] tbody tr')
          .first()
          .find('td')
          .first()
          .should('contain.text', 'C Entity');
        cy.get('[data-testid="entity-table"] tbody tr')
          .first()
          .find('td')
          .eq(1)
          .should('contain.text', DataReadinessStatus.VALIDATED_DATA);
      });
    });

    describe('Table with entity name filtering', () => {
      beforeEach(() => {
        cy.intercept(
          'POST',
          '/v1/data-readiness/entities',
          makeFakeEntityResponse({
            count: 2,
            overrideArrayItems: [
              {
                entityName: 'A Entity',
                dataReadinessStatus: DataReadinessStatus.NEEDS_REVIEW,
                children: [],
              },
              {
                entityName: 'B Entity',
                dataReadinessStatus: DataReadinessStatus.NOT_READY,
                children: [
                  {
                    entityName: 'B Entity Child',
                    dataReadinessStatus: DataReadinessStatus.NOT_READY,
                  },
                ],
              },
            ],
          })
        ).as('entityResponse');
        interceptsForTests();
        initGlobalMocks({ featureFlags: dataReadinessFeatureFlags });
        visitAndWait('/data-readiness');
        cy.wait('@periodResponse');
        cy.wait('@entityResponse', { timeout: TIME_TO_WAIT_FOR_BIG_FILES });
      });

      it('Filters by company entity', () => {
        cy.get('[data-testid="entity-table"] th').find('.ant-table-filter-trigger').first().click();

        // Select Entity A filter
        cy.get('.ant-dropdown-menu-item').contains('A Entity').click();

        //Click OK
        cy.get('.ant-btn-primary').contains('OK').click();

        // Verify that only Entity A is displayed
        cy.get('[data-testid="entity-table"] tbody tr').should('have.length', 1);
        cy.get('[data-testid="entity-table"] tbody tr')
          .first()
          .find('td')
          .first()
          .should('contain.text', 'A Entity');
      });

      it('Filters by divison entity', () => {
        cy.get('[data-testid="entity-table"] th').find('.ant-table-filter-trigger').first().click();

        // Select the Entity divisions for B filter
        cy.get('.ant-dropdown-menu-submenu').contains('B Entity Divisions').click();
        cy.get('.ant-dropdown-menu-item').contains('B Entity Child').click();

        //Click OK
        cy.get('.ant-btn-primary').contains('OK').click();

        // Verify that only whole Entity B record is shown
        cy.get('[data-testid="entity-table"] tbody tr').should('have.length', 2);
        cy.get('[data-testid="entity-table"] tbody tr')
          .first()
          .find('td')
          .first()
          .should('contain.text', 'B Entity');
      });
    });
  });
});

describe('Data Readiness Page No Data', () => {
  describe('No period config data', () => {
    beforeEach(() => {
      cy.intercept(
        'POST',
        '/v1/data-readiness/entities',
        makeFakeEntityResponse({
          count: 4,
        })
      ).as('entityResponse');
      cy.intercept(
        'GET',
        '/v1/period-configuration/tenant-periods',
        makeFakePeriodResponse({
          count: 0,
        })
      ).as('periodResponse');
      initGlobalMocks({ featureFlags: dataReadinessFeatureFlags });
      visitAndWait('/data-readiness');
    });

    it('Shows no data alert message', () => {
      cy.get('.vtx-alert-heading').should('contain.text', CONSTANTS.NO_DATA);
    });
  });
});

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/e2e/e2e.spec.ts`

```ts
describe('E2E', () => {
  it('should pass', () => {
    // eslint-disable-next-line @typescript-eslint/no-unused-expressions
    expect(true).to.be.true;
  });
});

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/page-objects/visit-and-wait.ts`

```ts
import { routeAliases } from 'cypress/mocked-api-routes/route-aliases';
import { isNotLoading } from './is-not-loading';

export const visitAndWait = (path: string, waitTime = 20000, waitForMenuLoading = true) => {
  cy.visit(path);
  cy.wait('@mfeModule', { timeout: waitTime });
  cy.wait(routeAliases.LaunchDarklyClientStreamGet.alias, { timeout: waitTime });
  cy.wait(routeAliases.LaunchDarklyGet.alias, { timeout: waitTime });
  cy.wait('@getUserPermissions', { timeout: waitTime });
  cy.wait('@getMenuItems', { timeout: waitTime });
  isNotLoading();
  if (waitForMenuLoading) {
    cy.get('[data-testid="side-menu-skeleton"]').should('not.exist');
  }
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/page-objects/select.ts`

```ts
import { Matcher } from '@testing-library/dom';

/**************
 * This File is for single select only
 *************/

/**
 * For use with deprecated select. This will click the drop down and choose an option
 */
export const deprecatedSelectOptionByLabel = (automationId: string, label: string) => {
  cy.getByTestId(automationId).click();
  cy.get(`.ant-select-item-option[title*="${label}"]`).click();
};

/** Finds select input by label, searches for an option, and selects it. */
export const selectOptionByLabel = (inputLabel: Matcher, optionLabel: string) => {
  cy.findByLabelText(inputLabel).as('selectInput');
  // click only using as a way to check when loader overlay is dropped
  cy.get('@selectInput').closest('[data-automation-class="vtx-select"]').click();
  cy.get('@selectInput').type(optionLabel);

  cy.get('.vtx-select-menu-portal').find('.vtx-menu-item').contains(optionLabel).click();
};

/**
 *  This should only be used if selectOptionByLabel does not work.
 *  Finds select input by automation id, searches for an option, and selects it.
 *  */
export const selectOptionByAutomationId = (automationId: string, optionLabel: string) => {
  cy.getByTestId(automationId).find('input[type="text"]').as('selectInput');
  // click only using as a way to check when loader overlay is dropped
  cy.get('@selectInput').closest('[data-automation-class="vtx-select"]').click();
  cy.get('@selectInput').type(optionLabel);

  cy.get('.vtx-select-menu-portal').find('.vtx-menu-item').contains(optionLabel).click();
};

export const checkSelectOptions = (id: string, optionLabels: string | string[]) => {
  cy.get(`#${id} > .vtx-select__control > .vtx-select__indicators`).click();

  cy.get('.vtx-select-menu-portal')
    .find('.vtx-menu-item')
    .should(($labels) => {
      const labelTexts = $labels.map((_, label) => Cypress.$(label).text()).get();
      expect(labelTexts).to.include.members(Array.isArray(optionLabels) ? optionLabels : [optionLabels]);
    });
};

function getInputElementByLabel(label: string) {
  return cy
    .contains('label', label)
    .should('be.visible')
    .then((labelElement) => {
      const labelID = labelElement.attr('for');
      return cy.get(`#${labelID}`).should('exist');
    });
}

export function selectDropdownValueTaxDataPage(formLabel: string, valueToSelect: string) {
  getInputElementByLabel(formLabel).then((inputElement) => {
    cy.wrap(inputElement).click();
    cy.wrap(inputElement).type(valueToSelect);
    cy.wrap(inputElement).type('{enter}');
  });
}

/**
 * Selects the Results per page value from Paginated Common Grid
 */
export const selectPaginationResultsPerPageByValue = (value: 10 | 20 | 50 | 100) => {
  cy.get('[data-testid="vtx-pagination__results-per-page"]')
    .find('div[data-automation-class="vtx-select"]')
    .click();
  cy.get('.vtx-select-menu-portal').find('.vtx-menu-item').contains(value).click();
};

/** Finds select input by label, searches for an option, and selects it. */
export const selectOptionByIndex = (inputLabel: Matcher, index: number) => {
  cy.findByLabelText(inputLabel).as('selectInput');
  // click only using as a way to check when loader overlay is dropped
  cy.get('@selectInput').closest('[data-automation-class="vtx-select"]').click();

  cy.get('.vtx-select-menu-portal').find('.vtx-menu-item').eq(index).click();
};

/** Finds select input by label and verifies the list of options it displays. */
export const checkSelectOptionsByInputLabel = (inputLabel: Matcher, optionLabels: string | string[]) => {
  cy.findByLabelText(inputLabel).as('selectInput');
  cy.get('@selectInput').closest('[data-automation-class="vtx-select"]').click();

  cy.get('.vtx-select-menu-portal')
    .find('.vtx-menu-item')
    .should(($labels) => {
      const labelTexts = $labels.map((_, label) => Cypress.$(label).text()).get();
      expect(labelTexts).to.include.members(Array.isArray(optionLabels) ? optionLabels : [optionLabels]);
    });
  cy.get('@selectInput').closest('[data-automation-class="vtx-select"]').click();
};

/** Finds select input by automation id, searches for an option by index, and selects it. */
export const selectOptionIndexByAutomationId = (automationId: string, index: number) => {
  cy.getByTestId(automationId).find('input[type="text"]').as('selectInput');
  // click only using as a way to check when loader overlay is dropped
  cy.get('@selectInput').closest('[data-automation-class="vtx-select"]').click();

  cy.get('.vtx-select-menu-portal').find('.vtx-menu-item').eq(index).click();
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/page-objects/module-overrides.ts`

```ts
export const setAppImportMapOverride = () => {
  localStorage.setItem('import-map-override:vtx-ui-mf-cnc-itc', '//localhost:9102/vtx-ui-mf-cnc-itc.js');
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/page-objects/login.ts`

```ts
import { makeFakeToken } from '../factories/token';

export const login = (username?: string) => {
  const tokenOverride = username ? { profile: { name: username } } : undefined;
  const token = makeFakeToken(tokenOverride);

  sessionStorage.setItem(Cypress.env('authSessionStorageKey'), JSON.stringify(token));
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/page-objects/tabs.ts`

```ts
export const selectTabByLabel = (label: string) => cy.get('[role="tab"]').contains(label).click();

export const getTabByLabel = (label: string) => cy.get('[role="tab"]').contains(label);

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/page-objects/internationalization.ts`

```ts
export const setupInternationalization = () => {
  localStorage.setItem('vtx-ui-mf-chrome:disable-region-reminder', 'true');
  localStorage.setItem('vtx-ui-mf-chrome:disable-region-setting-warning', 'true');
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/page-objects/analytics.ts`

```ts
export const setupAnalytics = () => {
  localStorage.setItem('vtx-ui-root-app:disable-analytics-tracking', 'true');
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/page-objects/subscriptions.ts`

```ts
import { makeFakeSubscriptionObject } from '../factories/subscription';
import { mockPlatformIntegrationProfileGetRoute } from '../mocked-api-routes/subscription';

export const setSubscriptions = () => {
  const subscriptionObject = makeFakeSubscriptionObject({
    subscription: {
      features: [
        {
          platformProductCode: 'tta-ind-tax-close',
          featureCode: '370',
          featureName: 'Indirect Tax Close',
        },
      ],
    },
    tenant: {
      type: 'Client',
      id: 'fake_tenant_id',
      subType: 'SMB',
    },
  });
  mockPlatformIntegrationProfileGetRoute(subscriptionObject);
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/page-objects/clients.ts`

```ts
import { makeFakeClient } from '../factories/client';
import { mockClientsGetRoute } from '../mocked-api-routes/client';

export const setClients = () => {
  const fakeClient = makeFakeClient({ isActiveClient: true });
  mockClientsGetRoute([fakeClient]);
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/page-objects/page-title.ts`

```ts
/**
 * Returns page title.
 */
export const getPageTitle = () => {
  return cy.get('[data-testid="page-title"]');
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/page-objects/is-not-loading.ts`

```ts
export const isNotLoading = () => {
  cy.get('.vtx-loading-indicator', { timeout: 30000 }).should('not.exist');
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/page-objects/feature-flags.ts`

```ts
import { FeatureFlagMFE } from 'src/feature-flag/feature-flag-keys';
import { FeatureFlag, makeFakeFeatureFlag } from '../factories/launchdarkly';

/*
 * These flags should always match the state of the LD portal since they
 * will be used for on-prem instances and any situation where the flags
 * can't be fetched.
 */

export const fakeFeatureFlags: Record<FeatureFlagMFE, FeatureFlag> = {
  'data-readiness-menu-item': makeFakeFeatureFlag({ value: false }),
  'data-files-menu-item': makeFakeFeatureFlag({ value: false }),
  'datasets-menu-item': makeFakeFeatureFlag({ value: false }),
  'source-systems-menu-item': makeFakeFeatureFlag({ value: false }),
  'data-functions-menu-item': makeFakeFeatureFlag({ value: false }),
  'enrichments-menu-item': makeFakeFeatureFlag({ value: false }),
  'configuration-menu-item': makeFakeFeatureFlag({ value: false }),
  'period-configuration-tab': makeFakeFeatureFlag({ value: false }),
  'entity-configuration-tab': makeFakeFeatureFlag({ value: false }),
  'maintenance-mode': makeFakeFeatureFlag({ value: false }),
  'indirect-tax-close-menu-item': makeFakeFeatureFlag({ value: false }),
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/page-objects/user-monitoring.ts`

```ts
export const setupUserMonitoring = () => {
  localStorage.setItem('vtx-ui-root-app:disable-user-monitoring', 'true');
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/page-objects/page-alert.ts`

```ts
export const getPageAlert = () => {
  return cy.get('[data-testid="page-alert"]');
};

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/config/qa.ts`

```ts
import { defineConfig } from 'cypress';
import { mergePartially } from 'merge-partially';
import baseConfig from './base';
import componentWebpack from './cypress.component.webpack.config';

export default defineConfig(
  mergePartially.shallow(baseConfig, {
    env: {
      authSessionStorageKey: 'oidc.user:https://qa-auth.vtxdev.net:TZiVuRuNKyRn7MSPiHgKgF7xXz9Ex2bv',
    },
    e2e: {
      baseUrl: 'https://qa-app.vtxdev.net/ui/transaction-tax-close',
    },
    component: {
      devServer: {
        framework: 'react',
        bundler: 'webpack',
        webpackConfig: componentWebpack('qa', 9002),
      },
    },
  })
);

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/config/e2e.ts`

```ts
import { defineConfig } from 'cypress';
import { mergePartially } from 'merge-partially';
import baseConfig from './base';

export default defineConfig(
  mergePartially.shallow(baseConfig, {
    e2e: {
      specPattern: 'cypress/e2e/**/*.spec.ts',
    },
  })
);

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/config/base.ts`

```ts
import webpackPreprocessor from '@cypress/webpack-preprocessor';
import { getWebpackPreprocessorOptions } from '@vertexinc/vtx-react-scripts';
import { defineConfig } from 'cypress';
import PluginEvents = Cypress.PluginEvents;
import PluginConfigOptions = Cypress.PluginConfigOptions;

// eslint-disable-next-line import/no-default-export
export default defineConfig({
  // These settings apply everywhere unless overridden
  chromeWebSecurity: false,
  fixturesFolder: 'cypress/fixtures',
  numTestsKeptInMemory: 2,
  projectId: 'frzj59',
  e2e: {
    specPattern: 'cypress/integration/**/*.spec.ts',
    supportFile: 'cypress/support/index.ts',
    setupNodeEvents(on, config) {
      // The following line allows for necessary values (eg. GitHub secrets like AUTH0_IDP_PASSWORD_DEVELOPMENT)
      // to be made available as Cypress environment variables.
      config.env = { ...config.env, ...process.env };

      const webpackPreprocessorOptions = getWebpackPreprocessorOptions();
      on('file:preprocessor', webpackPreprocessor(webpackPreprocessorOptions));

      return config;
    },
  },
  component: {
    devServer: {
      framework: 'react',
      bundler: 'webpack',
    },
    specPattern: 'cypress/component/**/*.cy.{ts,tsx}',
    supportFile: 'cypress/support/component.ts',
    setupNodeEvents(on: PluginEvents, config: PluginConfigOptions) {
      require('@cypress/code-coverage/task')(on, config);
      return config;
    },
  },
});

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/config/production.ts`

```ts
import { defineConfig } from 'cypress';
import { mergePartially } from 'merge-partially';
import baseConfig from './base';
import componentWebpack from './cypress.component.webpack.config';

export default defineConfig(
  mergePartially.shallow(baseConfig, {
    env: {
      authSessionStorageKey: 'oidc.user:https://auth.vertexcloud.com:Wp1IaTzLaDAxo2xZj6IioI3oI4yK0q6K',
    },
    e2e: {
      baseUrl: 'https://app.vertexcloud.com/ui/transaction-tax-close',
    },
    component: {
      devServer: {
        framework: 'react',
        bundler: 'webpack',
        webpackConfig: componentWebpack('production', 9002),
      },
    },
  })
);

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/config/development.ts`

```ts
import { defineConfig } from 'cypress';
import { mergePartially } from 'merge-partially';
import baseConfig from './base';
import componentWebpack from './cypress.component.webpack.config';

export default defineConfig(
  mergePartially.shallow(baseConfig, {
    env: {
      authSessionStorageKey: 'oidc.user:https://dev-auth.vtxdev.net:SgZmOOmYGqTdnXoE9i2w0t37PZr6VSEQ',
    },
    e2e: {
      baseUrl: 'https://dev-app.vtxdev.net/ui/transaction-tax-close',
    },
    component: {
      devServer: {
        framework: 'react',
        bundler: 'webpack',
        webpackConfig: componentWebpack('development', 9002),
      },
    },
  })
);

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/config/production-e2e.ts`

```ts
import { defineConfig } from 'cypress';
import { mergePartially } from 'merge-partially';
import prodConfig from './production';
import e2eConfig from './e2e';

export default defineConfig(mergePartially.shallow(prodConfig, e2eConfig));

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/config/staging-e2e.ts`

```ts
import { defineConfig } from 'cypress';
import { mergePartially } from 'merge-partially';
import stagConfig from './staging';
import e2eConfig from './e2e';

export default defineConfig(mergePartially.shallow(stagConfig, e2eConfig));

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/config/development-e2e.ts`

```ts
import { defineConfig } from 'cypress';
import { mergePartially } from 'merge-partially';
import devConfig from './development';
import e2eConfig from './e2e';

export default defineConfig(mergePartially.shallow(devConfig, e2eConfig));

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/config/qa-e2e.ts`

```ts
import { defineConfig } from 'cypress';
import { mergePartially } from 'merge-partially';
import qaConfig from './qa';
import e2eConfig from './e2e';

export default defineConfig(mergePartially.shallow(qaConfig, e2eConfig));

```

## 📄 `../vertexinc/vtx-ui-mf-cnc-itc/cypress/config/staging.ts`

```ts
import { defineConfig } from 'cypress';
import { mergePartially } from 'merge-partially';
import baseConfig from './base';
import componentWebpack from './cypress.component.webpack.config';

export default defineConfig(
  mergePartially.shallow(baseConfig, {
    env: {
      authSessionStorageKey: 'oidc.user:https://stage-auth.vertexcloud.com:lkWrJJx8FPAdJxLCPYdQ9GhyroGS4Sb7',
    },
    e2e: {
      baseUrl: 'https://stage-app.vertexcloud.com/ui/transaction-tax-close',
    },
    component: {
      devServer: {
        framework: 'react',
        bundler: 'webpack',
        webpackConfig: componentWebpack('staging', 9002),
      },
    },
  })
);

```

