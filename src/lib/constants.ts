import type { z } from 'astro/zod';
import MetaDefaultImage from '@/assets/images/meta-default.jpg';
import avatar from '@/assets/images/avatar.jpeg';
import type { seoSchemaWithoutImage } from '@/content.config';
import astroConfig from 'astro.config.mjs';

export type AuthorInfo = {
  name: string;
  avatar: any;
  headline: string;
  username?: string;
  location?: string;
  pronouns?: string;
}

export type Seo = z.infer<typeof seoSchemaWithoutImage> & {
  image?: any;
}

type DefaultConfigurationType = {
  baseUrl: string,
  author: AuthorInfo;
  seo: Seo;
}

export const DEFAULT_CONFIGURATION: DefaultConfigurationType = {
  baseUrl: astroConfig.site || 'https://iohel.com',
  author: {
    avatar,
    name: 'Joel Amoako',
    headline: 'Sofware Engineering',
    username: 'xceejay',
    location: 'Ghana, Accra',
    pronouns: 'He/Him',
  },
  seo: {
    title: 'My section of the internet',
    description: 'Clean and aesthetic portfolio website for developers and designers',
    type: 'website',
    image: MetaDefaultImage,
    twitter: {
      creator: '@joelkofiamoako'
    },
    robots: 'noindex, nofollow',
  }
};