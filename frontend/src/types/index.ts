/**
 * TypeScript types for AvtoMat Mini App
 */

export interface City {
  id: number;
  name: string;
  name_ru?: string;
  is_active: boolean;
}

export interface School {
  id: number;
  name: string;
  city: number;
  city_name: string;
  address: string;
  rating: string;
  trust_index: string;
  whatsapp?: string;
  telegram_contact?: string;
  payment_link_kaspi?: string;
  payment_link_halyk?: string;
  is_active: boolean;
}

export interface Instructor {
  id: number;
  name: string;
  city: number;
  city_name: string;
  auto_type: 'automatic' | 'manual';
  auto_type_display: string;
  phone: string;
  rating: string;
  payment_link_kaspi?: string;
  payment_link_halyk?: string;
  is_active: boolean;
}

export interface Application {
  id: number;
  student: number;
  school?: number;
  school_name?: string;
  instructor?: number;
  instructor_name?: string;
  city: number;
  city_name: string;
  category: string;
  format: 'online' | 'offline' | 'hybrid';
  format_display: string;
  time_slot?: string;
  status: string;
  status_display: string;
  student_name: string;
  student_phone: string;
  created_at: string;
  updated_at: string;
}

export interface ApplicationCreateData {
  telegram_id: number;
  school?: number;
  instructor?: number;
  city: number;
  category?: string;
  format?: 'online' | 'offline' | 'hybrid';
  time_slot?: string;
  student_name: string;
  student_phone: string;
}

export type FlowType = 'school' | 'instructor' | 'certificate';

